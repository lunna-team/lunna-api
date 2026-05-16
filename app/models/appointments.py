from sqlalchemy import Column, ForeignKey, Date, Time, DateTime, SmallInteger, String, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import AppointmentStatus, PatientAppointmentStatus, AppointmentType

class Appointment(BaseModel):
    __tablename__ = 'appointments'
    
    patient_id = Column(ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = Column(ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    clinic_id = Column(ForeignKey('clinics.id', ondelete='RESTRICT'), nullable=False)
    
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(SmallInteger, default=30)
    
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.pending)
    patient_status = Column(SQLEnum(PatientAppointmentStatus), default=PatientAppointmentStatus.pending)
    
    type = Column(SQLEnum(AppointmentType), default=AppointmentType.routine)
    location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    
    reschedule_reason = Column(String(255), nullable=True)
    reschedule_observation = Column(Text, nullable=True)
    reschedule_requested_at = Column(DateTime(timezone=True), nullable=True)
    reschedule_requested_by = Column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    reschedule_approved_at = Column(DateTime(timezone=True), nullable=True)
    reschedule_approved_by = Column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    new_date = Column(Date, nullable=True)
    new_time = Column(Time, nullable=True)
    
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancellation_reason = Column(String(255), nullable=True)
    
    # Relações
    patient = relationship("Patient")
    doctor = relationship("User", foreign_keys=[doctor_id])
    clinic = relationship("Clinic")
