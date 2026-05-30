import sys
import os
import hashlib
import secrets
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base, SessionLocal
from app.models import (
    Departamento, Rol, Empleado, EstadoActualEnum,
    UsuarioSistema
)

def simple_hash(password: str) -> str:
    """Genera hash de contraseña simple"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{hash_obj.hex()}"

def init_database():
    print("📦 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 1. Crear Departamentos
        print("\n📁 Creando departamentos...")
        deptos = [
            ('1', 'Producción'),
            ('2', 'Mantenimiento'),
            ('3', 'Logística'),
            ('4', 'Calidad'),
            ('5', 'Recursos Humanos'),
            ('6', 'Seguridad'),
            ('7', 'Sistemas'),
        ]
        for depto_id, nombre in deptos:
            existing = db.query(Departamento).filter(Departamento.id == depto_id).first()
            if not existing:
                depto = Departamento(id=depto_id, nombre=nombre)
                db.add(depto)
                print(f'   ✓ {nombre}')
        
        # 2. Crear Roles
        print("\n👥 Creando roles...")
        roles_data = [
            (1, 'Vigilante'),
            (2, 'Supervisor'),
            (3, 'RRHH'),
            (4, 'Administrador'),
            (5, 'Superusuario'),
        ]
        for rol_id, nombre in roles_data:
            existing = db.query(Rol).filter(Rol.id == rol_id).first()
            if not existing:
                rol = Rol(id=rol_id, nombre=nombre)
                db.add(rol)
                print(f'   ✓ {nombre}')
        
        db.commit()
        
        # 3. Crear Empleados
        print("\n👨‍💼 Creando empleados...")
        empleados_data = [
            ('1001', 'Juan Martínez', '1', 'Operador'),
            ('1002', 'María González', '1', 'Supervisor de Producción'),
            ('1003', 'Carlos López', '2', 'Técnico Mantenimiento'),
            ('1004', 'Ana Rodríguez', '3', 'Coordinador Logística'),
            ('1005', 'Pedro Sánchez', '4', 'Inspector Calidad'),
            ('1006', 'Laura Fernández', '5', 'Asistente RRHH'),
            ('1007', 'Roberto Méndez', '2', 'Mecánico'),
            ('1008', 'Patricia Soto', '3', 'Almacenista'),
            ('1009', 'Jorge Ramírez', '6', 'Guardia Seguridad'),
            ('1010', 'Silvia Torres', '7', 'Desarrollador'),
        ]
        
        for num, nombre, depto_id, puesto in empleados_data:
            existing = db.query(Empleado).filter(Empleado.numero_empleado == num).first()
            if not existing:
                empleado = Empleado(
                    numero_empleado=num,
                    nombre_completo=nombre,
                    departamento_id=depto_id,
                    puesto=puesto,
                    estado_actual=EstadoActualEnum.FUERA,
                    activo=True
                )
                db.add(empleado)
                print(f'   ✓ {num}: {nombre}')
        
        db.commit()
        
        # 4. Crear Usuarios del Sistema
        print("\n🔐 Creando usuarios del sistema...")
        usuarios_data = [
            ('admin', 'Admin123!', 5, None),
            ('vigilante1', 'Vig123!', 1, '1009'),
            ('supervisor1', 'Sup123!', 2, '1002'),
            ('rrhh1', 'RRHH123!', 3, '1006'),
            ('admin2', 'Admin456!', 4, '1010'),
        ]
        
        for username, password, rol_id, emp_num in usuarios_data:
            existing = db.query(UsuarioSistema).filter(UsuarioSistema.username == username).first()
            if not existing:
                empleado = None
                if emp_num:
                    empleado = db.query(Empleado).filter(Empleado.numero_empleado == emp_num).first()
                
                usuario = UsuarioSistema(
                    username=username,
                    password_hash=simple_hash(password),
                    rol_id=rol_id,
                    empleado_id=empleado.id if empleado else None,
                    activo=True
                )
                db.add(usuario)
                print(f'   ✓ {username} (Rol: {rol_id})')
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ BASE DE DATOS INICIALIZADA CON ÉXITO")
        print("="*60)
        print("\n📋 EMPLEADOS REGISTRADOS (para escanear):")
        for num, nombre, _, _ in empleados_data:
            print(f"   🔹 {num} - {nombre}")
        
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("   👑 Administrador:     admin / Admin123!")
        print("   👁️ Vigilante:         vigilante1 / Vig123!")
        print("   👔 Supervisor:        supervisor1 / Sup123!")
        print("   📊 RRHH:              rrhh1 / RRHH123!")
        print("   💻 Administrador 2:   admin2 / Admin456!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        print("\n✨ Inicialización completada")

if __name__ == "__main__":
    init_database()
