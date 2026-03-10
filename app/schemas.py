from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import LeaseStatus, UserRole


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=10, max_length=128)
    role: UserRole = UserRole.TENANT


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ParcelCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    location: str = Field(min_length=3, max_length=200)
    area_hectares: float = Field(gt=0)
    monthly_price: float = Field(gt=0)


class ParcelRead(ParcelCreate):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class LeaseCreate(BaseModel):
    parcel_id: int
    start_date: date
    end_date: date

    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, value: date, info):
        start_date = info.data.get('start_date')
        if start_date and value <= start_date:
            raise ValueError('end_date must be after start_date')
        return value


class LeaseRead(BaseModel):
    id: int
    parcel_id: int
    tenant_id: int
    start_date: date
    end_date: date
    status: LeaseStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LeaseStatusUpdate(BaseModel):
    status: LeaseStatus
