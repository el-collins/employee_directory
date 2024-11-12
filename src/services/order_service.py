# src/services/order_service.py
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.schemas.order_schema import OrderCreate, OrderStatus
from src.core.models.order import Order
from sqlalchemy import func
from typing import Optional

class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_total_revenue(self, start_date: datetime, end_date: datetime) -> float:
        """
        Calculate total revenue for orders within the given date range.
        
        Args:
            start_date: Start date for revenue calculation
            end_date: End date for revenue calculation
            
        Returns:
            float: Total revenue for the period
        """
        total_revenue = (
            self.db.query(func.sum(Order.amount))
            .filter(Order.order_date >= start_date)
            .filter(Order.order_date <= end_date)
            .filter(Order.status != OrderStatus.CANCELLED)
            .scalar() or 0.0
        )
        return round(float(total_revenue), 2)

    def create_order(self, order_data: OrderCreate) -> Optional[Order]:
        """
        Create a new order.
        
        Args:
            order_data: OrderCreate schema containing order details
            
        Returns:
            Order: Created order object
            
        Raises:
            ValueError: If order creation fails due to validation
        """
        try:
            new_order = Order(
                customer_id=order_data.customer_id,
                amount=order_data.amount,
                status=order_data.status,
                order_date=order_data.order_date,
                created_at=datetime.utcnow()
            )
            self.db.add(new_order)
            self.db.commit()
            self.db.refresh(new_order)
            return new_order
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create order: {str(e)}")