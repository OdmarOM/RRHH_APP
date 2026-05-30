from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import models
import schemas
from database import engine, get_db

# Inicializar Base de Datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de RRHH y Vigilancia",
    description="API robusta para terminales Zebra y Panel Web",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que cualquier frontend se conecte (ideal para desarrollo local)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Sistema"])
def leer_raiz():
    return {"status": "online", "mensaje": "Núcleo del sistema activo."}

# ==========================================
# MÓDULO ADMINISTRATIVO (RRHH / ADMIN)
# ==========================================

@app.post("/api/v1/admin/departamentos", response_model=schemas.DepartamentoOut, tags=["Admin - Catálogos"])
def crear_departamento(depto: schemas.DepartamentoCreate, db: Session = Depends(get_db)):
    if db.query(models.Departamento).filter(models.Departamento.nombre == depto.nombre).first():
        raise HTTPException(status_code=400, detail="El departamento ya existe")
    nuevo_depto = models.Departamento(nombre=depto.nombre)
    db.add(nuevo_depto)
    db.commit()
    db.refresh(nuevo_depto)
    return nuevo_depto

@app.post("/api/v1/admin/empleados", response_model=schemas.EmpleadoOut, tags=["Admin - Catálogos"])
def crear_empleado(empleado: schemas.EmpleadoCreate, db: Session = Depends(get_db)):
    if db.query(models.Empleado).filter(models.Empleado.numero_empleado == empleado.numero_empleado).first():
        raise HTTPException(status_code=400, detail="El número de empleado ya está en uso")
    nuevo_empleado = models.Empleado(**empleado.model_dump())
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado

@app.get("/api/v1/admin/empleados", response_model=list[schemas.EmpleadoOut], tags=["Admin - Catálogos"])
def listar_empleados(db: Session = Depends(get_db)):
    return db.query(models.Empleado).all()


# ==========================================
# MÓDULO DE CASETA (TERMINALES ZEBRA)
# ==========================================

@app.post("/api/v1/caseta/empleados/escanear/{numero_empleado}", response_model=schemas.EmpleadoOut, tags=["Caseta - Operación Diaria"])
def escanear_empleado(numero_empleado: str, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.numero_empleado == numero_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@app.post("/api/v1/caseta/empleados/entrada/{empleado_id}", tags=["Caseta - Operación Diaria"])
def registrar_entrada(empleado_id: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if empleado.estado_actual != models.EstadoEmpleadoEnum.Fuera:
        raise HTTPException(status_code=400, detail=f"El empleado ya está registrado como: {empleado.estado_actual}")

    ahora = datetime.now(timezone.utc)
    # NOTA: Aquí iría la lógica de evaluar la tabla TurnosHorarios para definir si es "Normal" o "En_Espera_Pase"
    # Por ahora, registramos entrada normal como base.
    
    nueva_asistencia = models.RegistroAsistencia(
        empleado_id=empleado.id,
        fecha_turno=ahora.date(),
        hora_entrada_real=ahora,
        estado_registro=models.EstadoRegistroEnum.Normal
    )
    
    empleado.estado_actual = models.EstadoEmpleadoEnum.Adentro
    db.add(nueva_asistencia)
    db.commit()
    return {"mensaje": "Entrada registrada exitosamente", "estado": empleado.estado_actual}

@app.post("/api/v1/caseta/empleados/salida-final/{empleado_id}", tags=["Caseta - Operación Diaria"])
def registrar_salida(empleado_id: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not empleado or empleado.estado_actual != models.EstadoEmpleadoEnum.Adentro:
        raise HTTPException(status_code=400, detail="El empleado no está adentro de la planta")

    # Buscar la asistencia abierta de hoy
    asistencia = db.query(models.RegistroAsistencia).filter(
        models.RegistroAsistencia.empleado_id == empleado_id,
        models.RegistroAsistencia.hora_salida_real == None
    ).order_by(models.RegistroAsistencia.id.desc()).first()

    if asistencia:
        asistencia.hora_salida_real = datetime.now(timezone.utc)
        
    empleado.estado_actual = models.EstadoEmpleadoEnum.Fuera
    db.commit()
    return {"mensaje": "Jornada terminada correctamente"}

@app.post("/api/v1/caseta/empleados/observacion-rapida", tags=["Caseta - Operación Diaria"])
def observacion_rapida(datos: schemas.ObservacionCreate, db: Session = Depends(get_db)):
    asistencia = db.query(models.RegistroAsistencia).filter(
        models.RegistroAsistencia.empleado_id == datos.empleado_id,
        models.RegistroAsistencia.hora_salida_real == None
    ).order_by(models.RegistroAsistencia.id.desc()).first()

    if not asistencia:
        raise HTTPException(status_code=400, detail="No hay turno activo para registrar observación")

    nueva_obs = models.ObservacionCaseta(
        asistencia_id=asistencia.id,
        tipo_observacion=datos.tipo_observacion
    )
    db.add(nueva_obs)
    db.commit()
    return {"mensaje": f"Observación '{datos.tipo_observacion}' registrada."}

# ==========================================
# MÓDULO DE EXTERNOS (PROVEEDORES Y FILA)
# ==========================================

@app.post("/api/v1/caseta/externos/registrar", response_model=schemas.ExternoOut, tags=["Caseta - Externos"])
def registrar_externo(externo: schemas.ExternoCreate, db: Session = Depends(get_db)):
    nuevo_externo = models.FilaExterno(**externo.model_dump())
    db.add(nuevo_externo)
    db.commit()
    db.refresh(nuevo_externo)
    return nuevo_externo

@app.get("/api/v1/caseta/externos/fila", response_model=list[schemas.ExternoOut], tags=["Caseta - Externos"])
def ver_fila_externos(db: Session = Depends(get_db)):
    return db.query(models.FilaExterno).filter(
        models.FilaExterno.estado_fila == models.EstadoFilaEnum.Espera_Amarillo
    ).order_by(models.FilaExterno.hora_llegada.asc()).all()

@app.put("/api/v1/caseta/externos/{externo_id}/asignar-acceso", tags=["Caseta - Externos"])
def asignar_acceso_externo(externo_id: int, datos: schemas.ExternoAsignar, db: Session = Depends(get_db)):
    externo = db.query(models.FilaExterno).filter(models.FilaExterno.id == externo_id).first()
    if not externo:
        raise HTTPException(status_code=404, detail="Registro externo no encontrado")
    
    externo.estado_fila = models.EstadoFilaEnum.Adentro_Verde
    externo.anden_asignado = datos.anden_asignado
    externo.hora_entrada = datetime.now(timezone.utc)
    db.commit()
    return {"mensaje": f"Acceso concedido. Dirigirse a {datos.anden_asignado}"}