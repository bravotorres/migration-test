
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.data.models import Commerce, Employee
from src.data.schemas import EmployeeList, EmployeeOne, EmployeeNew, EmployeeUpdate


def make_employee_one(employee: Employee) -> EmployeeOne:
    """
    Conversion for Model to Schema.
    :param employee: Model to conversed a Schema (by the nombre_completo field)
    :return: Schema
    """
    return EmployeeOne(
        id=UUID(employee.uuid),
        nombre_completo=f"{employee.nombre} {employee.apellidos}",
        pin=employee.pin,
        fecha_creacion=employee.fecha_creacion,
        activo=employee.activo
    )


def get_employee_list(commerce: Commerce) -> EmployeeList:
    """
    Get list of all Employees by Commerce
    :param commerce:
    :return: Schema of list of Schemas
    """
    employees = commerce.trabajadores

    employee_lst = []
    for employee in employees:
        employee_lst.append(make_employee_one(employee))

    e_list = EmployeeList(employees=employee_lst)

    return e_list


def get_employee(dbs: Session, commerce_id: int, employee_uuid: UUID) -> EmployeeOne:
    """
    Obtains an Employee by UUID
    :param dbs:
    :param commerce_id:
    :param employee_uuid:
    :return: Employee Schema
    """
    employee = dbs.query(Employee). \
        filter(Employee.comercio_id == commerce_id). \
        filter(Employee.uuid == employee_uuid.hex). \
        first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee not found.")

    return make_employee_one(employee)


def create_employee(db: Session, commerce_id: int, employee: EmployeeNew):
    try:
        db_employee = Employee(comercio_id=commerce_id, **employee.dict())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        employee_one = make_employee_one(db_employee)

        return employee_one
    except IntegrityError as ie:
        detail = f"Duplicated 'pin'. Can't be saved, "
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    except Exception as e:
        detail = f"Employee '{employee.nombre} {employee.apellidos}' can't be saved."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def update_employee(db: Session, commerce: Commerce, uuid_empleado: UUID, employee: EmployeeUpdate):
    """
    Update Employee by UUID and data provided by schema.
    :param db:
    :param commerce:
    :param uuid_empleado:
    :param employee:
    :return:
    """
    try:
        db_employee = db.query(Employee). \
            filter(Employee.comercio_id == commerce.id). \
            filter(Employee.uuid == uuid_empleado.hex). \
            first()

        if not db_employee:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee not found.")

        db_employee.nombre = employee.nombre
        db_employee.apellidos = employee.apellidos
        db_employee.pin = employee.pin
        db_employee.activo = employee.activo

        db.commit()
        db.refresh(db_employee)

        employee_one = make_employee_one(db_employee)
        return employee_one
    except HTTPException as he:
        raise he
    except Exception as e:
        detail = f"Employee '{employee.nombre} {employee.apellidos}' can't be updated."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def delete_employee(db: Session, commerce: Commerce, uuid_empleado: UUID):
    """
    Delete Employee by UUID.
    :param db:
    :param commerce:
    :param uuid_empleado:
    :return:
    """
    try:
        db_employee = db.query(Employee). \
            filter(Employee.comercio_id == commerce.id). \
            filter(Employee.uuid == uuid_empleado.hex). \
            delete()

        if not db_employee:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee not found.")

        db.commit()
        return
    except HTTPException as he:
        raise he
    except Exception as e:
        detail = f"Error, can't be deleted."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
