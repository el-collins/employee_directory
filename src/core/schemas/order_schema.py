# src/core/schemas/order_schema.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderCreate(BaseModel):
    customer_id: UUID
    amount: float = Field(gt=0)
    status: OrderStatus
    order_date: datetime

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    amount: float
    status: OrderStatus
    order_date: datetime
    created_at: datetime

    class Config:
        orm_mode = True