from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Clinic(BaseModel):
    __tablename__ = 'clinics'
    
    name = Column(String(255), nullable=False)
    logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(7), nullable=True)
    secondary_color = Column(String(7), nullable=True)
    accent_color = Column(String(7), nullable=True)
    
    address = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    timezone = Column(String(50), default='America/Sao_Paulo')
    language = Column(String(10), default='pt-BR')
    
    users = relationship("User", back_populates="clinic")
