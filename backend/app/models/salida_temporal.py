from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class SalidaTemporal(Base):
    __tablename__ = "salidas_temporales"
    
    id = Column(Integer, primary_key=True, index=True)
    asistencia_id = Column(Integer, ForeignKey("registro_asistencias.id"))
    tipo_salida = Column(String(50))
    hora_salida = Column(DateTime(timezone=True))
    hora_regreso = Column(DateTime(timezone=True))
    estado_salida = Column(String(50))
