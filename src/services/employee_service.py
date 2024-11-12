from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime
from src.core.exceptions import EmployeeNotFoundException
from src.core.models.employee import Employee
from src.core.schemas.employee_schema import EmployeeCreate, EmployeeUpdate
import uuid


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_employees(self) -> list[Employee]:
        employees = self.db.query(Employee).all()
        for employee in employees:
            if employee.updated_at is None:
                employee.updated_at = employee.created_at
        return employees

    def get_employee_by_id(self, id: uuid.UUID) -> Employee:
        employee = self.db.query(Employee).filter(Employee.id == id).first()
        if not employee:
            raise EmployeeNotFoundException(id)
        return employee

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        db_employee = Employee(
            **employee.dict(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(db_employee)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Employee with email {employee.email} already exists")
        self.db.refresh(db_employee)
        return db_employee

    def update_employee(self, id: uuid.UUID, employee: EmployeeUpdate) -> Employee:
        db_employee = self.get_employee_by_id(id)
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db_employee.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def delete_employee(self, id: uuid.UUID):
        db_employee = self.get_employee_by_id(id)
        self.db.delete(db_employee)
        self.db.commit()