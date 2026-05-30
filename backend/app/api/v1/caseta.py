from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
from app.core.database import get_db
from app.models.empleado import Empleado, EstadoActualEnum
from app.models.asistencia import RegistroAsistencia, EstadoRegistroEnum
from app.models.turno import TurnoHorario
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class EscaneoResponse(BaseModel):
    empleado: str
    estado: str
    mensaje: str
    pase_expira: Optional[datetime] = None
    es_retardo: bool = False

@router.post("/escanear/{gafete}")
async def escanear_empleado(
    gafete: str,
    db: Session = Depends(get_db)
):
    # Buscar empleado
    empleado = db.query(Empleado).filter(
        Empleado.numero_empleado == gafete,
        Empleado.activo == True
    ).first()
    
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    # Obtener hora actual en zona horaria local
    tz = pytz.timezone("America/Mexico_City")
    ahora = datetime.now(tz)
    dia_semana = ahora.weekday()
    
    # Buscar turno del empleado para hoy
    turno = db.query(TurnoHorario).filter(
        TurnoHorario.empleado_id == empleado.id,
        TurnoHorario.dia_semana == dia_semana
    ).first()
    
    # Caso 1: Empleado en día libre (sin turno configurado)
    if not turno:
        asistencia = RegistroAsistencia(
            empleado_id=empleado.id,
            fecha_turno=ahora,
            hora_entrada_real=ahora,
            estado_registro=EstadoRegistroEnum.VISITA_DESCANSO,
            validacion_supervisor=True
        )
        db.add(asistencia)
        empleado.estado_actual = EstadoActualEnum.ADENTRO
        db.commit()
        
        return EscaneoResponse(
            empleado=empleado.nombre_completo,
            estado="ADENTRO",
            mensaje=f"✓ Registro de visita - Día libre (Sin turno configurado)"
        )
    
    # Calcular hora límite con tolerancia
    hora_oficial = ahora.replace(
        hour=turno.hora_entrada_oficial.hour,
        minute=turno.hora_entrada_oficial.minute,
        second=0,
        microsecond=0
    )
    tolerancia = timedelta(minutes=turno.tolerancia_minutos)
    limite_tolerancia = hora_oficial + tolerancia
    
    # Caso 2: Retardo
    if ahora > limite_tolerancia:
        pase_expira = ahora + timedelta(minutes=30)
        empleado.estado_actual = EstadoActualEnum.EN_ESPERA_PASE
        
        asistencia = RegistroAsistencia(
            empleado_id=empleado.id,
            fecha_turno=ahora,
            estado_registro=EstadoRegistroEnum.RETARDO_APROBADO,
            pase_espera_expira=pase_expira,
            validacion_supervisor=False
        )
        db.add(asistencia)
        db.commit()
        
        return EscaneoResponse(
            empleado=empleado.nombre_completo,
            estado="EN_ESPERA_PASE",
            mensaje=f"⚠️ RETARDO detectado! Debe ser aprobado por supervisor antes de las {pase_expira.strftime('%H:%M')}",
            pase_expira=pase_expira,
            es_retardo=True
        )
    
    # Caso 3: Entrada normal
    asistencia = RegistroAsistencia(
        empleado_id=empleado.id,
        fecha_turno=ahora,
        hora_entrada_real=ahora,
        estado_registro=EstadoRegistroEnum.NORMAL,
        validacion_supervisor=True
    )
    db.add(asistencia)
    empleado.estado_actual = EstadoActualEnum.ADENTRO
    db.commit()
    
    hora_limite = limite_tolerancia.strftime('%H:%M')
    return EscaneoResponse(
        empleado=empleado.nombre_completo,
        estado="ADENTRO",
        mensaje=f"✓ Entrada registrada - Hora límite: {hora_limite}"
    )

@router.post("/aprobar-pase/{asistencia_id}")
async def aprobar_pase(asistencia_id: int, db: Session = Depends(get_db)):
    """Supervisor aprueba pase por retardo"""
    asistencia = db.query(RegistroAsistencia).filter(
        RegistroAsistencia.id == asistencia_id,
        RegistroAsistencia.estado_registro == EstadoRegistroEnum.RETARDO_APROBADO
    ).first()
    
    if not asistencia:
        raise HTTPException(status_code=404, detail="Pase no encontrado")
    
    tz = pytz.timezone("America/Mexico_City")
    ahora = datetime.now(tz)
    
    if ahora > asistencia.pase_espera_expira:
        asistencia.estado_registro = EstadoRegistroEnum.INCIDENCIA
        db.commit()
        raise HTTPException(status_code=400, detail="❌ Pase expirado - Incidencia generada")
    
    asistencia.hora_entrada_real = ahora
    asistencia.validacion_supervisor = True
    
    empleado = db.query(Empleado).filter(Empleado.id == asistencia.empleado_id).first()
    empleado.estado_actual = EstadoActualEnum.ADENTRO
    
    db.commit()
    
    return {
        "message": "✓ Pase aprobado exitosamente",
        "empleado": empleado.nombre_completo
    }
