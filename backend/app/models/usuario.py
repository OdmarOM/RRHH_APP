from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class UsuarioSistema(Base):
    __tablename__ = "usuarios_sistema"
    
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    activo = Column(Boolean, default=True)
    
    # Relationships
    empleado = relationship("Empleado", back_populates="usuario_sistema")
    rol = relationship("Rol")
