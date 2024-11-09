from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_id: int
    amount: float
    status: str
    order_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)