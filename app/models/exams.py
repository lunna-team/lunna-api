from sqlalchemy import Column, ForeignKey, Date, SmallInteger, String, Text, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import UltrasoundType, FetalPresentation, VaccineStatus

class Ultrasound(BaseModel):
    __tablename__ = 'ultrasounds'
    
    patient_id = Column(ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = Column(ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    
    type = Column(SQLEnum(UltrasoundType), nullable=False)
    date = Column(Date, nullable=False)
    ig_weeks = Column(SmallInteger, nullable=False)
    
    presentation = Column(SQLEnum(FetalPresentation), nullable=True)
    placenta_location = Column(String(100), nullable=True)
    amniotic_fluid_ml = Column(Numeric(7, 2), nullable=True)
    fetal_heart_rate = Column(SmallInteger, nullable=True)
    fetal_weight_g = Column(Numeric(7, 2), nullable=True)
    percentile = Column(SmallInteger, nullable=True)
    
    image_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    patient = relationship("Patient")
    doctor = relationship("User", foreign_keys=[doctor_id])

class Vaccine(BaseModel):
    __tablename__ = 'vaccines'
    
    patient_id = Column(ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = Column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    vaccine_type = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    
    dose_number = Column(SmallInteger, nullable=True)
    status = Column(SQLEnum(VaccineStatus), default=VaccineStatus.scheduled)
    reactions = Column(Text, nullable=True)

    patient = relationship("Patient")
