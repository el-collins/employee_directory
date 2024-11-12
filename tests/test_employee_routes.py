# tests/test_employee_routes.py
import pytest
from uuid import UUID

@pytest.fixture
def sample_employee_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "department": "Engineering"
    }

@pytest.mark.asyncio
async def test_create_employee(async_client, sample_employee_data):
    response = await async_client.post("/api/v1/employees", json=sample_employee_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_employee_data["email"]
    assert data["first_name"] == sample_employee_data["first_name"]
    assert UUID(data["id"])  # Verify UUID format
    return data

@pytest.mark.asyncio
async def test_list_employees(async_client, sample_employee_data):
    # First create an employee
    await async_client.post("/api/v1/employees", json=sample_employee_data)
    
    response = await async_client.get("/api/v1/employees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "email" in data[0]

@pytest.mark.asyncio
async def test_get_employee(async_client, sample_employee_data):
    # First create an employee
    create_response = await async_client.post("/api/v1/employees", json=sample_employee_data)
    employee_id = create_response.json()["id"]
    
    response = await async_client.get(f"/api/v1/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json()["id"] == employee_id

@pytest.mark.asyncio
async def test_update_employee(async_client, sample_employee_data):
    # First create an employee
    create_response = await async_client.post("/api/v1/employees", json=sample_employee_data)
    employee_id = create_response.json()["id"]
    
    updated_data = {
        "first_name": "Jane",
        "department": "Management"
    }
    
    response = await async_client.put(f"/api/v1/employees/{employee_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == updated_data["first_name"]
    assert data["department"] == updated_data["department"]
    assert data["last_name"] == sample_employee_data["last_name"]  # Unchanged field

@pytest.mark.asyncio
async def test_delete_employee(async_client, sample_employee_data):
    # First create an employee
    create_response = await async_client.post("/api/v1/employees", json=sample_employee_data)
    employee_id = create_response.json()["id"]
    
    # Delete the employee
    response = await async_client.delete(f"/api/v1/employees/{employee_id}")
    assert response.status_code == 204
    
    # Verify employee is deleted
    get_response = await async_client.get(f"/api/v1/employees/{employee_id}")
    assert get_response.status_code == 404