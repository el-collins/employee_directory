# src/services/order_service.py
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.models.order import Order
from sqlalchemy import func

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
            .scalar() or 0.0
        )
        return float(total_revenue)