from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, engine, get_db
from app.dependencies import get_current_user, rate_limit_login, require_roles
from app.models import LandParcel, Lease, LeaseStatus, User, UserRole
from app.schemas import (
    LeaseCreate,
    LeaseRead,
    LeaseStatusUpdate,
    LoginRequest,
    ParcelCreate,
    ParcelRead,
    Token,
    UserCreate,
    UserRead,
)
from app.security import create_access_token, hash_password, verify_password

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['Authorization', 'Content-Type'],
)


@app.middleware('http')
async def secure_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'same-origin'
    response.headers['Content-Security-Policy'] = "default-src 'none'"
    return response


@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get('/healthz')
def health_check():
    return {'status': 'ok'}


@app.post('/auth/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db), _: None = Depends(rate_limit_login)):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post('/auth/login', response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db), _: None = Depends(rate_limit_login)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    token = create_access_token(str(user.id))
    return Token(access_token=token)


@app.post('/parcels', response_model=ParcelRead, status_code=status.HTTP_201_CREATED)
def create_parcel(
    payload: ParcelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.OWNER, UserRole.ADMIN)),
):
    parcel = LandParcel(**payload.model_dump(), owner_id=current_user.id)
    db.add(parcel)
    db.commit()
    db.refresh(parcel)
    return parcel


@app.get('/parcels', response_model=list[ParcelRead])
def list_parcels(db: Session = Depends(get_db)):
    return db.query(LandParcel).all()


@app.post('/leases', response_model=LeaseRead, status_code=status.HTTP_201_CREATED)
def request_lease(
    payload: LeaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TENANT, UserRole.ADMIN)),
):
    parcel = db.query(LandParcel).filter(LandParcel.id == payload.parcel_id).first()
    if parcel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parcel not found')

    overlap_exists = (
        db.query(Lease)
        .filter(
            Lease.parcel_id == payload.parcel_id,
            Lease.status.in_([LeaseStatus.PENDING, LeaseStatus.ACTIVE]),
            Lease.start_date <= payload.end_date,
            Lease.end_date >= payload.start_date,
        )
        .first()
    )
    if overlap_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Parcel already has an overlapping lease')

    lease = Lease(**payload.model_dump(), tenant_id=current_user.id)
    db.add(lease)
    db.commit()
    db.refresh(lease)
    return lease


@app.patch('/leases/{lease_id}/status', response_model=LeaseRead)
def update_lease_status(
    lease_id: int,
    payload: LeaseStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.OWNER, UserRole.ADMIN)),
):
    lease = db.query(Lease).filter(Lease.id == lease_id).first()
    if lease is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lease not found')

    if current_user.role != UserRole.ADMIN and lease.parcel.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Cannot update lease for another owner')

    lease.status = payload.status
    db.add(lease)
    db.commit()
    db.refresh(lease)
    return lease


@app.delete('/parcels/{parcel_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.OWNER, UserRole.ADMIN)),
):
    parcel = db.query(LandParcel).filter(LandParcel.id == parcel_id).first()
    if parcel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parcel not found')

    if current_user.role != UserRole.ADMIN and parcel.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Cannot delete parcel you do not own')

    db.delete(parcel)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
