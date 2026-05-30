from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Departamento(Base):
    __tablename__ = "departamentos"
    
    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    
    empleados = relationship("Empleado", back_populates="departamento")
