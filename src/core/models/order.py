from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from src.core.schemas.order_schema import OrderStatus



class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID
    amount: float = Field(gt=0)
    status: OrderStatus
    order_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)