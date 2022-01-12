from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.data.base import Base


class Commerce(Base):
    __tablename__ = "main_comercio"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(64), nullable=False, default=uuid4().__str__())
    nombre = Column(String(128), nullable=False)
    activo = Column(Boolean, default=True)
    email_contacto = Column(String(50), nullable=True)
    telefono_contacto = Column(String(16), nullable=True)
    api_key = Column(String(64), nullable=False, default=uuid4().__str__())
    fecha_creacion = Column(DateTime, default=datetime.now())

    trabajadores = relationship("Employee", back_populates="pertenece")


class Employee(Base):
    __tablename__ = "main_empleado"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(64), nullable=False, default=uuid4().hex)
    nombre = Column(String(32), nullable=False)
    apellidos = Column(String(32), nullable=False)
    pin = Column(String(6), nullable=False, unique=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now())
    activo = Column(Boolean, default=True)
    comercio_id = Column(Integer, ForeignKey("main_comercio.id"))

    pertenece = relationship("Commerce", back_populates="trabajadores")
