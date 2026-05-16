from typing import Optional
from datetime import date
from uuid import UUID
from pydantic import EmailStr, Field
from app.schemas.base import CoreModel, BaseEntitySchema
from app.models.enums import UserRole

# -- User --

class UserBase(CoreModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.patient
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserCreate(UserBase):
    password: str
    clinic_id: UUID

class UserUpdate(CoreModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase, BaseEntitySchema):
    clinic_id: UUID
    is_active: bool

# -- Patient --

class PatientCreate(CoreModel):
    doctor_id: UUID
    prontuario: str
    lmp_date: date
    edd: date
    height_cm: Optional[str] = None
    weight_initial_kg: Optional[str] = None
    imc: Optional[str] = None
    blood_type: Optional[str] = None
    acompanhante: Optional[str] = None
    hospital: Optional[str] = None

class PatientResponse(PatientCreate, BaseEntitySchema):
    user_id: UUID
    current_week: Optional[int] = None
    
# -- Clinic --

class ClinicBase(CoreModel):
    name: str
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None

class ClinicCreate(ClinicBase):
    pass

class ClinicResponse(ClinicBase, BaseEntitySchema):
    pass
