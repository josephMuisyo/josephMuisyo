from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, Enum):
    OWNER = 'owner'
    TENANT = 'tenant'
    ADMIN = 'admin'


class LeaseStatus(str, Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    REJECTED = 'rejected'
    TERMINATED = 'terminated'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.TENANT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    parcels: Mapped[list['LandParcel']] = relationship(back_populates='owner', cascade='all, delete-orphan')


class LandParcel(Base):
    __tablename__ = 'land_parcels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    area_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    monthly_price: Mapped[float] = mapped_column(Float, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    owner: Mapped['User'] = relationship(back_populates='parcels')
    leases: Mapped[list['Lease']] = relationship(back_populates='parcel', cascade='all, delete-orphan')


class Lease(Base):
    __tablename__ = 'leases'
    __table_args__ = (
        UniqueConstraint('parcel_id', 'tenant_id', 'start_date', name='uq_lease_dedupe'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    parcel_id: Mapped[int] = mapped_column(ForeignKey('land_parcels.id', ondelete='CASCADE'), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[LeaseStatus] = mapped_column(SAEnum(LeaseStatus), default=LeaseStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    parcel: Mapped['LandParcel'] = relationship(back_populates='leases')
    tenant: Mapped['User'] = relationship()
