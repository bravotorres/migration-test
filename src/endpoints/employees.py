from fastapi.routing import APIRouter
from fastapi import Depends, Response, status
from pydantic.schema import UUID

from src.config.dependencies import get_db, get_api_key
from sqlalchemy.orm import Session
from src.data.models import Commerce, Employee
from src.data.schemas import EmployeeList, EmployeeOne, EmployeeNew, EmployeeUpdate
from src.endpoints.business import get_employee_list, get_employee, create_employee, update_employee, delete_employee

router = APIRouter(
    prefix="/empleados",
    tags=["empleados"],
)


@router.post("/")
def public_new_employee(employee: EmployeeNew, commerce: Commerce = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    CREATE Employee
    :param employee:
    :param commerce:
    :param db:
    :return:
    """
    new_employee = create_employee(db, commerce.id, employee)

    response_body = {
        "rc": 0,
        "msg": "Ok!",
        "data": new_employee
    }

    return response_body


@router.get("/")
def read_all_employees(commerce: Commerce = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    READ ALL Employees
    :param commerce: Commerce necessary to proceed.
    :param db: Database session.
    :return:
    NOTE: Not filtered by CommerceID
    """

    employee_list = get_employee_list(commerce)

    response_body = {
        "rc": 0,
        "msg": "Ok!",
        "data": employee_list.employees
    }
    return response_body


@router.get("/{uuid_empleado}")
def read_employee(uuid_empleado: UUID, commerce: Commerce = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    READ Employee
    :param uuid_empleado: UUID to search Employee
    :param commerce: API Key access
    :param db:
    :return:
    """

    employee = get_employee(db, commerce.id, uuid_empleado)

    response_body = {
        "rc": 0,
        "msg": "Ok!",
        "data": employee
    }

    return response_body


@router.put("/{uuid_empleado}")
def public_new_employee(uuid_empleado: UUID, employee: EmployeeUpdate, commerce: Commerce = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    UPDATE Employee
    :param uuid_empleado: 
    :param employee: 
    :param commerce: 
    :param db: 
    :return: 
    """
    employee_updated = update_employee(db, commerce, uuid_empleado, employee)

    response_body = {
        "rc": 0,
        "msg": "Ok!",
        "data": employee_updated
    }

    return response_body


@router.delete("/{uuid_empleado}")
def public_new_employee(uuid_empleado: UUID, commerce: Commerce = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    DELETE Employee
    :param uuid_empleado:
    :param commerce:
    :param db:
    :return:
    """
    delete_employee(db, commerce, uuid_empleado)

    response_body = {
        "rc": 0,
        "msg": "Ok!"
    }

    return response_body
