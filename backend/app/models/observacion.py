from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class ObservacionCaseta(Base):
    __tablename__ = "observaciones_caseta"
    
    id = Column(Integer, primary_key=True, index=True)
    asistencia_id = Column(Integer, ForeignKey("registro_asistencias.id"))
    tipo_observacion = Column(String(100))
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
