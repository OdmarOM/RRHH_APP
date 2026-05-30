from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class SupervisorDepartamento(Base):
    __tablename__ = "supervisores_departamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios_sistema.id"))
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
