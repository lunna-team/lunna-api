from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class CoreModel(BaseModel):
    """
    Base para todos os schemas Pydantic
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BaseEntitySchema(CoreModel):
    """
    Schema base para entidades do banco (com id e timestamps)
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
