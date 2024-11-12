from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class OrderCreate(BaseModel):
    customer_id: UUID
    amount: float
    status: str
    order_date: datetime

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    amount: float
    status: str
    order_date: datetime
    created_at: datetime

    class Config:
        orm_mode = True