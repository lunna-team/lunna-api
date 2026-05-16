from sqlalchemy import Column, ForeignKey, Date, Time, SmallInteger, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import VitalClassification, TimeOfDay, GlucoseMoment

class Contraction(BaseModel):
    __tablename__ = 'contractions'
    
    patient_id = Column(ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    
    duration_seconds = Column(SmallInteger, nullable=False)
    interval_minutes = Column(Numeric(5, 2), nullable=True)
    session_date = Column(Date, nullable=False)

    patient = relationship("Patient")

class GlucoseReading(BaseModel):
    __tablename__ = 'glucose_readings'
    
    patient_id = Column(ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    
    value_mg_dl = Column(Numeric(5, 2), nullable=False)
    moment = Column(SQLEnum(GlucoseMoment), nullable=False)
    classification = Column(SQLEnum(VitalClassification), nullable=False)
    notes = Column(Text, nullable=True)

    patient = relationship("Patient")

class BloodPressureReading(BaseModel):
    __tablename__ = 'blood_pressure_readings'
    
    patient_id = Column(ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    
    systolic = Column(SmallInteger, nullable=False)
    diastolic = Column(SmallInteger, nullable=False)
    pulse_bpm = Column(SmallInteger, nullable=True)
    
    moment = Column(SQLEnum(TimeOfDay), nullable=False)
    classification = Column(SQLEnum(VitalClassification), nullable=False)

    patient = relationship("Patient")
