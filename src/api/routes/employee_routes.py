from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.core.schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from src.services.employee_service import EmployeeService

router = APIRouter()

@router.get("/employees", response_model=list[EmployeeResponse])
async def list_employees(db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    return employee_service.get_all_employees()

@router.get("/employees/{id}", response_model=EmployeeResponse)
async def get_employee(id: int, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    return employee_service.get_employee_by_id(id)

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    return employee_service.create_employee(employee)

@router.put("/employees/{id}", response_model=EmployeeResponse)
async def update_employee(id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    return employee_service.update_employee(id, employee)

@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(id: int, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    employee_service.delete_employee(id)
    return {}