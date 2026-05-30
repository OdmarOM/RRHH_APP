from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class EstadoRegistroEnum(str, enum.Enum):
    NORMAL = "Normal"
    RETARDO_APROBADO = "Retardo_Aprobado"
    INCIDENCIA = "Incidencia"
    VISITA_DESCANSO = "Visita_Descanso"

class RegistroAsistencia(Base):
    __tablename__ = "registro_asistencias"
    
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    fecha_turno = Column(DateTime(timezone=True), nullable=False)
    hora_entrada_real = Column(DateTime(timezone=True))
    hora_salida_real = Column(DateTime(timezone=True))
    estado_registro = Column(Enum(EstadoRegistroEnum), default=EstadoRegistroEnum.NORMAL)
    pase_espera_expira = Column(DateTime(timezone=True))
    minutos_extra_calculados = Column(Integer, default=0)
    validacion_supervisor = Column(Boolean, default=False)
    validacion_rrhh = Column(Boolean, default=False)
    
    empleado = relationship("Empleado")
