from datetime import datetime, timedelta
from sqlalchemy import func, cast, DATE
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.clinic import Clinic
from app.models.user import User
from app.models.appointments import Appointment
from app.models.enums import UserRole
from app.schemas.metrics import PlatformOverview, PlatformGrowthChart, TimeSeriesDataPoint

async def get_platform_overview(db: AsyncSession) -> PlatformOverview:
    """
    Recupera os totais globais da plataforma.
    """
    # 1. Total Clínicas
    clinics_stmt = select(func.count(Clinic.id)).where(Clinic.deleted_at == None)
    clinics_count = (await db.execute(clinics_stmt)).scalar()
    
    # 2. Total Pacientes
    patients_stmt = (
        select(func.count(User.id))
        .where(User.role == UserRole.patient)
        .where(User.deleted_at == None)
    )
    patients_count = (await db.execute(patients_stmt)).scalar()
    
    # 3. Total Médicos
    doctors_stmt = (
        select(func.count(User.id))
        .where(User.role == UserRole.doctor)
        .where(User.deleted_at == None)
    )
    doctors_count = (await db.execute(doctors_stmt)).scalar()
    
    # 4. Total Consultas
    appointments_stmt = select(func.count(Appointment.id)).where(Appointment.deleted_at == None)
    appointments_count = (await db.execute(appointments_stmt)).scalar()
    
    return PlatformOverview(
        total_clinics=clinics_count or 0,
        total_patients=patients_count or 0,
        total_doctors=doctors_count or 0,
        total_appointments=appointments_count or 0
    )

async def get_platform_growth(db: AsyncSession) -> PlatformGrowthChart:
    """
    Recupera dados de crescimento (consultas e pacientes) dos últimos 30 dias.
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Consultas nos últimos 30 dias agrupadas por dia
    stmt_appointments = (
        select(cast(Appointment.created_at, DATE).label("day"), func.count(Appointment.id))
        .where(Appointment.created_at >= thirty_days_ago)
        .where(Appointment.deleted_at == None)
        .group_by(cast(Appointment.created_at, DATE))
        .order_by("day")
    )
    res_appointments = await db.execute(stmt_appointments)
    appointments_data = [
        TimeSeriesDataPoint(date=row[0].isoformat(), count=row[1]) 
        for row in res_appointments.all()
    ]
    
    # Novos pacientes nos últimos 30 dias agrupados por dia
    stmt_patients = (
        select(cast(User.created_at, DATE).label("day"), func.count(User.id))
        .where(User.role == UserRole.patient)
        .where(User.created_at >= thirty_days_ago)
        .where(User.deleted_at == None)
        .group_by(cast(User.created_at, DATE))
        .order_by("day")
    )
    res_patients = await db.execute(stmt_patients)
    patients_data = [
        TimeSeriesDataPoint(date=row[0].isoformat(), count=row[1]) 
        for row in res_patients.all()
    ]
    
    return PlatformGrowthChart(
        appointments_last_30_days=appointments_data,
        new_patients_last_30_days=patients_data
    )
