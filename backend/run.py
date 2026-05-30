import uvicorn
from app.core.database import engine, Base
from app.models import Departamento, Rol, Empleado

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente")
    
    print("\nIniciando servidor FastAPI...")
    print("API Documentation: http://localhost:8000/docs")
    print("Presiona Ctrl+C para detener el servidor\n")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )