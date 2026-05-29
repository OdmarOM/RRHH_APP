from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class RolEnum(str, enum.Enum):
    Vigilante = "Vigilante"
    Supervisor = "Supervisor"
    RRHH = "RRHH"
    Administrador = "Administrador"
    Superusuario = "Superusuario"

class EstadoEmpleadoEnum(str, enum.Enum):
    Fuera = "Fuera"
    Adentro = "Adentro"
    Salida_Temporal = "Salida_Temporal"
    En_Espera_Pase = "En_Espera_Pase"

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum(RolEnum), unique=True, index=True)

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    empleados = relationship("Empleado", back_populates="departamento")

class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True, index=True)
    numero_empleado = Column(String, unique=True, index=True)
    nombre_completo = Column(String, index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    puesto = Column(String)
    foto_url = Column(String, nullable=True)
    estado_actual = Column(Enum(EstadoEmpleadoEnum), default=EstadoEmpleadoEnum.Fuera)
    activo = Column(Boolean, default=True)

    departamento = relationship("Departamento", back_populates="empleados")
    usuario = relationship("UsuarioSistema", back_populates="empleado", uselist=False)

class UsuarioSistema(Base):
    __tablename__ = "usuarios_sistema"
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    activo = Column(Boolean, default=True)

    empleado = relationship("Empleado", back_populates="usuario")
    rol = relationship("Rol")