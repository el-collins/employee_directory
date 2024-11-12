from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class Employee(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    department: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default=None, nullable=True)