# src/api/routes/order_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.schemas.order_schema import OrderCreate, OrderResponse
from src.database.connection import get_db
from src.services.order_service import OrderService

router = APIRouter()


def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use MM/DD/YYYY",
        )


@router.get("/orders/revenue", response_model=dict[str, float])
async def get_revenue(
    start_date: str = Query(
        ...,
        description="Start date for revenue calculation (format: MM/DD/YYYY), eg. 11/11/2024",
    ),
    end_date: str = Query(
        ...,
        description="End date for revenue calculation (format: MM/DD/YYYY) e.g. 11/12/2024",
    ),
    db: Session = Depends(get_db),
):
    """
    Get total revenue within a specified date range.

    - **start_date**: Start date for revenue calculation (inclusive). Format: MM/DD/YYYY
    - **end_date**: End date for revenue calculation (inclusive). Format: MM/DD/YYYY
    - **db**: Database session dependency.

    Returns a dictionary with the total revenue.
    """
    start_date_parsed = parse_date(start_date)
    end_date_parsed = parse_date(end_date)

    if end_date_parsed < start_date_parsed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be earlier than start date",
        )

    order_service = OrderService(db)
    total_revenue = order_service.get_total_revenue(start_date_parsed, end_date_parsed)
    return {"total_revenue": total_revenue}


@router.post(
    "/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED
)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.

    - **order**: OrderCreate schema containing order details.
    - **db**: Database session dependency.

    Returns the created order details.

    Status:
    "pending",
    "confirmed",
    "shipped",
    "delivered",
    "cancelled",

    exmaple:
    {
        "customer_id": "5b8f4a9d-1c7a-4c1f-8a1d-1f1e4b1b4b2d",
        "amount": 100.0,
        "status": "confirmed",
        "order_date": "2024-11-11T00:00:00"
    }
    """
    order_service = OrderService(db)
    try:
        new_order = order_service.create_order(order)
        return new_order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the order",
        )


# get all orders route
@router.get("/orders", response_model=list[OrderResponse])
async def get_orders(db: Session = Depends(get_db)):
    """
    Get all orders.

    - **db**: Database session dependency.

    Returns a list of all orders.
    """
    order_service = OrderService(db)
    return order_service.get_orders()
