from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from models import (
    RolEnum, EstadoEmpleadoEnum, EstadoRegistroEnum, 
    TipoSalidaEnum, EstadoSalidaEnum, TipoVisitanteEnum, EstadoFilaEnum
)

# --- DEPARTAMENTOS ---
class DepartamentoCreate(BaseModel):
    nombre: str

class DepartamentoOut(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

# --- EMPLEADOS ---
class EmpleadoCreate(BaseModel):
    numero_empleado: str
    nombre_completo: str
    departamento_id: int
    puesto: str
    foto_url: Optional[str] = None

class EmpleadoOut(BaseModel):
    id: int
    numero_empleado: str
    nombre_completo: str
    puesto: str
    estado_actual: EstadoEmpleadoEnum
    activo: bool
    model_config = ConfigDict(from_attributes=True)

# --- ASISTENCIAS ---
class AsistenciaOut(BaseModel):
    id: int
    empleado_id: int
    fecha_turno: date
    hora_entrada_real: Optional[datetime]
    hora_salida_real: Optional[datetime]
    estado_registro: EstadoRegistroEnum
    model_config = ConfigDict(from_attributes=True)

# --- OBSERVACIONES ---
class ObservacionCreate(BaseModel):
    empleado_id: int
    tipo_observacion: str

# --- SALIDAS TEMPORALES ---
class SalidaTemporalCreate(BaseModel):
    empleado_id: int
    tipo_salida: TipoSalidaEnum

# --- EXTERNOS (FILA) ---
class ExternoCreate(BaseModel):
    tipo_visitante: TipoVisitanteEnum
    nombre_empresa: str
    nombre_chofer: str

class ExternoAsignar(BaseModel):
    anden_asignado: str

class ExternoOut(BaseModel):
    id: int
    tipo_visitante: TipoVisitanteEnum
    nombre_empresa: str
    nombre_chofer: str
    estado_fila: EstadoFilaEnum
    anden_asignado: Optional[str]
    hora_llegada: datetime
    model_config = ConfigDict(from_attributes=True)