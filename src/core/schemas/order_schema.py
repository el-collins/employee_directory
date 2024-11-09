from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    customer_id: int
    amount: float
    status: str
    order_date: datetime

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    amount: float
    status: str
    order_date: datetime
    created_at: datetime

    class Config:
        orm_mode = True