# src/api/routes/order_routes.py
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.services.order_service import OrderService

router = APIRouter()

@router.get("/orders/revenue")
async def get_revenue(
    start_date: datetime = Query(..., description="Start date for revenue calculation"),
    end_date: datetime = Query(..., description="End date for revenue calculation"),
    db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    total_revenue = order_service.get_total_revenue(start_date, end_date)
    return {"total_revenue": total_revenue}

