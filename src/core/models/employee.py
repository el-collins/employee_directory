from sqlmodel import SQLModel, Field
from datetime import datetime

class Employee(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    department: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default=None, nullable=True)