from sqlalchemy import Column, Integer, ForeignKey, Time
from app.core.database import Base

class TurnoHorario(Base):
    __tablename__ = "turnos_horarios"
    
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    dia_semana = Column(Integer)
    hora_entrada_oficial = Column(Time)
    hora_salida_oficial = Column(Time)
    tolerancia_minutos = Column(Integer, default=15)
