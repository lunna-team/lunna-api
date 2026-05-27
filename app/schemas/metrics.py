from typing import List
from pydantic import Field
from app.schemas.base import CoreModel

class PlatformOverview(CoreModel):
    total_clinics: int = Field(..., description="Total de clínicas cadastradas na plataforma.")
    total_patients: int = Field(..., description="Total de pacientes (gestantes) em todas as clínicas.")
    total_doctors: int = Field(..., description="Total de médicos cadastrados na plataforma.")
    total_appointments: int = Field(..., description="Total de consultas realizadas/agendadas na plataforma.")

class TimeSeriesDataPoint(CoreModel):
    date: str = Field(..., description="Data no formato YYYY-MM-DD.", examples=["2026-05-01"])
    count: int = Field(..., description="Quantidade de registros para esta data.")

class PlatformGrowthChart(CoreModel):
    appointments_last_30_days: List[TimeSeriesDataPoint] = Field(..., description="Histórico de consultas nos últimos 30 dias.")
    new_patients_last_30_days: List[TimeSeriesDataPoint] = Field(..., description="Histórico de novas pacientes nos últimos 30 dias.")
