from app.core.database import SessionLocal
from app.models.asistencia import RegistroAsistencia, EstadoRegistroEnum
from app.models.empleado import Empleado
from datetime import datetime
import pytz

db = SessionLocal()

print("\n🔍 INCIDENCIAS PENDIENTES DE APROBACIÓN")
print("="*50)

pendientes = db.query(RegistroAsistencia).filter(
    RegistroAsistencia.estado_registro == EstadoRegistroEnum.RETARDO_APROBADO,
    RegistroAsistencia.validacion_supervisor == False
).all()

if pendientes:
    for p in pendientes:
        empleado = db.query(Empleado).filter(Empleado.id == p.empleado_id).first()
        print(f"\n📋 ID: {p.id}")
        print(f"   Empleado: {empleado.nombre_completo}")
        print(f"   Fecha: {p.fecha_turno.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Expira: {p.pase_espera_expira.strftime('%H:%M:%S')}")
        
        # Verificar si ya expiró
        tz = pytz.timezone('America/Mexico_City')
        if datetime.now(tz) > p.pase_espera_expira:
            print(f"   ⚠️ EXPIRADO - Incidencia generada")
            p.estado_registro = EstadoRegistroEnum.INCIDENCIA
            db.commit()
        else:
            print(f"   ⏰ Vigente - Se puede aprobar")
else:
    print("\n✓ No hay incidencias pendientes")

db.close()
