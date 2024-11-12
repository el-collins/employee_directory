import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.core.schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from src.services.employee_service import EmployeeService
from src.core.exceptions import EmployeeNotFoundException

router = APIRouter()

@router.get("/employees", response_model=list[EmployeeResponse])
async def list_employees(db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    return employee_service.get_all_employees()

@router.get("/employees/{id}", response_model=EmployeeResponse)
async def get_employee(id: uuid.UUID, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    try:
        return employee_service.get_employee_by_id(id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    try:
        return employee_service.create_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee with this email already exists")


@router.put("/employees/{id}", response_model=EmployeeResponse)
async def update_employee(id: uuid.UUID, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    try:
        return employee_service.update_employee(id, employee)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(id: uuid.UUID, db: Session = Depends(get_db)):
    employee_service = EmployeeService(db)
    try:
        employee_service.delete_employee(id)
        return {}
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    