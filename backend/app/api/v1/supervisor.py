from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.asistencia import RegistroAsistencia, EstadoRegistroEnum
from app.models.empleado import Empleado, EstadoActualEnum
from app.services.auth_service import AuthService
from datetime import datetime
import pytz

router = APIRouter(prefix="/api/v1/supervisor", tags=["Supervisor"])

@router.get("/incidencias")
async def get_incidencias(db: Session = Depends(get_db)):
    pendientes = db.query(RegistroAsistencia).filter(
        RegistroAsistencia.estado_registro == EstadoRegistroEnum.RETARDO_APROBADO,
        RegistroAsistencia.validacion_supervisor == False
    ).all()
    
    resultado = []
    tz = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz)
    
    for p in pendientes:
        empleado = db.query(Empleado).filter(Empleado.id == p.empleado_id).first()
        
        # Verificar expiración
        if ahora > p.pase_espera_expira and p.pase_espera_expira:
            p.estado_registro = EstadoRegistroEnum.INCIDENCIA
            db.commit()
            continue
            
        resultado.append({
            "id": p.id,
            "empleado_nombre": empleado.nombre_completo if empleado else "Desconocido",
            "fecha_turno": p.fecha_turno.isoformat(),
            "pase_expira": p.pase_espera_expira.isoformat() if p.pase_espera_expira else None
        })
    
    return resultado

@router.post("/aprobar-pase/{asistencia_id}")
async def aprobar_pase(asistencia_id: int, db: Session = Depends(get_db)):
    asistencia = db.query(RegistroAsistencia).filter(
        RegistroAsistencia.id == asistencia_id
    ).first()
    
    if not asistencia:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    tz = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz)
    
    if asistencia.pase_espera_expira and ahora > asistencia.pase_espera_expira:
        asistencia.estado_registro = EstadoRegistroEnum.INCIDENCIA
        db.commit()
        raise HTTPException(status_code=400, detail="Pase expirado")
    
    asistencia.hora_entrada_real = ahora
    asistencia.validacion_supervisor = True
    asistencia.estado_registro = EstadoRegistroEnum.RETARDO_APROBADO
    
    empleado = db.query(Empleado).filter(Empleado.id == asistencia.empleado_id).first()
    if empleado:
        empleado.estado_actual = EstadoActualEnum.ADENTRO
    
    db.commit()
    
    return {"message": "Pase aprobado exitosamente"}

# Router para RRHH
router2 = APIRouter(prefix="/api/v1/rrhh", tags=["RRHH"])

@router2.get("/asistencias")
async def get_asistencias(db: Session = Depends(get_db)):
    asistencias = db.query(RegistroAsistencia).order_by(
        RegistroAsistencia.fecha_turno.desc()
    ).limit(50).all()
    
    resultado = []
    for a in asistencias:
        empleado = db.query(Empleado).filter(Empleado.id == a.empleado_id).first()
        resultado.append({
            "id": a.id,
            "empleado_nombre": empleado.nombre_completo if empleado else "Desconocido",
            "fecha_turno": a.fecha_turno.isoformat(),
            "hora_entrada_real": a.hora_entrada_real.isoformat() if a.hora_entrada_real else None,
            "estado_registro": a.estado_registro.value if a.estado_registro else "N/A"
        })
    
    return resultado
