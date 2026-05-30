from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class EstadoActualEnum(str, enum.Enum):
    FUERA = "Fuera"
    ADENTRO = "Adentro"
    SALIDA_TEMPORAL = "Salida_Temporal"
    EN_ESPERA_PASE = "En_Espera_Pase"

class Empleado(Base):
    __tablename__ = "empleados"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_empleado = Column(String(20), unique=True, nullable=False)
    nombre_completo = Column(String(200), nullable=False)
    departamento_id = Column(String, ForeignKey("departamentos.id"))
    puesto = Column(String(100))
    estado_actual = Column(Enum(EstadoActualEnum), default=EstadoActualEnum.FUERA)
    activo = Column(Boolean, default=True)
    
    # Relationships
    departamento = relationship("Departamento", back_populates="empleados")
    usuario_sistema = relationship("UsuarioSistema", back_populates="empleado", uselist=False)
