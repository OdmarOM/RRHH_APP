from app.core.database import SessionLocal
from app.models.turno import TurnoHorario
from app.models.empleado import Empleado
from datetime import time

db = SessionLocal()

try:
    # Obtener empleados
    empleados = db.query(Empleado).all()
    
    # Configurar turnos para cada empleado
    turnos_config = [
        # (empleado_id, dia_semana, hora_entrada, hora_salida, tolerancia)
        (1, 0, '08:00', '17:00', 15),   # Lunes
        (1, 1, '08:00', '17:00', 15),   # Martes
        (1, 2, '08:00', '17:00', 15),   # Miércoles
        (1, 3, '08:00', '17:00', 15),   # Jueves
        (1, 4, '08:00', '17:00', 15),   # Viernes
    ]
    
    for empleado in empleados[:5]:  # Para los primeros 5 empleados
        for dia in range(5):  # Lunes a Viernes
            turno = TurnoHorario(
                empleado_id=empleado.id,
                dia_semana=dia,
                hora_entrada_oficial=time(8, 0),  # 8:00 AM
                hora_salida_oficial=time(17, 0),  # 5:00 PM
                tolerancia_minutos=15
            )
            db.add(turno)
            print(f'✓ Turno agregado para {empleado.nombre_completo} - Día {dia}')
    
    db.commit()
    print('\n✅ Turnos configurados exitosamente')
    
except Exception as e:
    print(f'Error: {e}')
    db.rollback()
finally:
    db.close()
