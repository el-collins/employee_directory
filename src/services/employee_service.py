# src/services/employee_service.py
from sqlalchemy.orm import Session
from src.core.models.employee import Employee
from src.core.schemas.employee_schema import EmployeeCreate, EmployeeUpdate

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_employees(self) -> list[Employee]:
        return self.db.query(Employee).all()

    def get_employee_by_id(self, id: int) -> Employee:
        return self.db.query(Employee).filter(Employee.id == id).first()

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        db_employee = Employee(**employee.dict())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def update_employee(self, id: int, employee: EmployeeUpdate) -> Employee:
        db_employee = self.get_employee_by_id(id)
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def delete_employee(self, id: int):
        db_employee = self.get_employee_by_id(id)
        self.db.delete(db_employee)
        self.db.commit()
