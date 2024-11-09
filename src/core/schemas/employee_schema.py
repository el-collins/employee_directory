from pydantic import BaseModel
from datetime import datetime

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str

class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True