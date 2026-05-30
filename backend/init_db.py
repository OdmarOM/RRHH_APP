from app.core.database import SessionLocal, engine
from app.models import Base
from app.models.rol import Rol
from app.models.usuario import UsuarioSistema
from app.services.auth_service import AuthService

def init_database():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Crear roles
        roles = ["Vigilante", "Supervisor", "RRHH", "Administrador", "Superusuario"]
        for rol_nombre in roles:
            rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
            if not rol:
                rol = Rol(nombre=rol_nombre)
                db.add(rol)
        
        db.commit()
        
        # Crear superusuario inicial
        superuser = db.query(UsuarioSistema).filter(
            UsuarioSistema.username == "admin"
        ).first()
        
        if not superuser:
            superuser = UsuarioSistema(
                username="admin",
                password_hash=AuthService.get_password_hash("Admin123!"),
                rol_id=5,  # Superusuario
                activo=True
            )
            db.add(superuser)
            db.commit()
            
        print("Base de datos inicializada correctamente")
        
    finally:
        db.close()

if __name__ == "__main__":
    init_database()