from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None

class EmployeeResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    department: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True