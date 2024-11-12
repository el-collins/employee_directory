# tests/test_order_routes.py
from uuid import UUID, uuid4
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def sample_order_data():
    return {
        "customer_id": str(uuid4()),
        "amount": 100.0,
        "status": "confirmed",
        "order_date": datetime.utcnow().isoformat()
    }

@pytest.mark.asyncio
async def test_create_order(async_client, sample_order_data):
    response = await async_client.post("/api/v1/orders", json=sample_order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == sample_order_data["amount"]
    assert UUID(data["id"])
    return data

@pytest.mark.asyncio
async def test_get_revenue(async_client, sample_order_data):
    # Create some test orders
    await async_client.post("/api/v1/orders", json=sample_order_data)
    
    # Test revenue calculation
    today = datetime.now()
    start_date = (today - timedelta(days=30)).strftime("%m/%d/%Y")
    end_date = today.strftime("%m/%d/%Y")
    
    response = await async_client.get(
        "/api/v1/orders/revenue",
        params={"start_date": start_date, "end_date": end_date}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert isinstance(data["total_revenue"], (int, float))
    assert data["total_revenue"] > 0

@pytest.mark.asyncio
async def test_create_order_invalid_amount(async_client, sample_order_data):
    invalid_order = sample_order_data.copy()
    invalid_order["amount"] = -100.0
    
    response = await async_client.post("/api/v1/orders", json=invalid_order)
    assert response.status_code == 400
    assert "Amount must be greater than 0" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_order_invalid_status(async_client, sample_order_data):
    invalid_order = sample_order_data.copy()
    invalid_order["status"] = "invalid_status"
    
    response = await async_client.post("/api/v1/orders", json=invalid_order)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_revenue_invalid_date_format(async_client):
    response = await async_client.get(
        "/api/v1/orders/revenue",
        params={
            "start_date": "2023-01-01",  # Invalid format
            "end_date": "2023-12-31"
        }
    )
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]