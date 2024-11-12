import uuid

class EmployeeNotFoundException(Exception):
    def __init__(self, employee_id: uuid.UUID):
        self.employee_id = employee_id
        self.message = f"Employee with id {employee_id} not found"
        super().__init__(self.message)