from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class FilaExterno(Base):
    __tablename__ = "fila_externos"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_visitante = Column(String(50))
    nombre_empresa = Column(String(100))
    estado_fila = Column(String(50))
    anden_asignado = Column(String(20))
    hora_llegada = Column(DateTime(timezone=True), server_default=func.now())
