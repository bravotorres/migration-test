from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic.schema import UUID


class EmployeeOne(BaseModel):
    """
    List of all Employees
    HTTP_GET
    """
    id: UUID
    nombre_completo: str
    pin: str
    fecha_creacion: datetime
    activo: bool


class EmployeeList(BaseModel):
    """
    List of all Employees
    HTTP_GET
    """
    employees: List[EmployeeOne]


class EmployeeNew(BaseModel):
    """
    Base Employee Schema
    """
    nombre: str
    apellidos: str
    pin: str

    class Config:
        orm_mode = True


class EmployeeUpdate(EmployeeNew):
    """
    Base Employee Schema
    """
    activo: bool
