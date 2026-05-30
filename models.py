from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime, timezone

# --- ENUMS ---
class RolEnum(str, enum.Enum):
    Vigilante = "Vigilante"
    Supervisor = "Supervisor"
    RRHH = "RRHH"
    Administrador = "Administrador"
    Superusuario = "Superusuario"

class EstadoEmpleadoEnum(str, enum.Enum):
    Fuera = "Fuera"
    Adentro = "Adentro"
    Salida_Temporal = "Salida_Temporal"
    En_Espera_Pase = "En_Espera_Pase"

class EstadoRegistroEnum(str, enum.Enum):
    Normal = "Normal"
    Retardo_Aprobado = "Retardo_Aprobado"
    Incidencia = "Incidencia"
    Visita_Descanso = "Visita_Descanso"

class TipoSalidaEnum(str, enum.Enum):
    Mandado_Trabajo = "Mandado_Trabajo"
    Permiso_Personal = "Permiso_Personal"

class EstadoSalidaEnum(str, enum.Enum):
    Abierta = "Abierta"
    Cerrada = "Cerrada"
    Anulada_Por_Sistema = "Anulada_Por_Sistema"

class TipoVisitanteEnum(str, enum.Enum):
    Proveedor = "Proveedor"
    Servicio = "Servicio"
    Cliente = "Cliente"

class EstadoFilaEnum(str, enum.Enum):
    Espera_Amarillo = "Espera_Amarillo"
    Adentro_Verde = "Adentro_Verde"
    Retirado = "Retirado"
    Rechazado = "Rechazado"

# --- MODELOS ---
class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum(RolEnum), unique=True, index=True)

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    empleados = relationship("Empleado", back_populates="departamento")

class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True, index=True)
    numero_empleado = Column(String, unique=True, index=True)
    nombre_completo = Column(String, index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    puesto = Column(String)
    foto_url = Column(String, nullable=True)
    estado_actual = Column(Enum(EstadoEmpleadoEnum), default=EstadoEmpleadoEnum.Fuera)
    activo = Column(Boolean, default=True)

    departamento = relationship("Departamento", back_populates="empleados")
    usuario = relationship("UsuarioSistema", back_populates="empleado", uselist=False)

class UsuarioSistema(Base):
    __tablename__ = "usuarios_sistema"
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    activo = Column(Boolean, default=True)

    empleado = relationship("Empleado", back_populates="usuario")
    rol = relationship("Rol")

class SupervisorDepartamento(Base):
    __tablename__ = "supervisores_departamentos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios_sistema.id"))
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))

class TurnoHorario(Base):
    __tablename__ = "turnos_horarios"
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    dia_semana = Column(Integer) # 0=Lunes, 6=Domingo
    hora_entrada_oficial = Column(String) # Ej: "08:00"
    hora_salida_oficial = Column(String) # Ej: "18:00"
    tolerancia_minutos = Column(Integer, default=15)

class RegistroAsistencia(Base):
    __tablename__ = "registro_asistencias"
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    fecha_turno = Column(Date, index=True)
    hora_entrada_real = Column(DateTime, nullable=True)
    hora_salida_real = Column(DateTime, nullable=True)
    estado_registro = Column(Enum(EstadoRegistroEnum), default=EstadoRegistroEnum.Normal)
    pase_espera_expira = Column(DateTime, nullable=True)
    minutos_extra_calculados = Column(Integer, default=0)
    validacion_supervisor = Column(Boolean, default=False)
    validacion_rrhh = Column(Boolean, default=False)
    bloqueado = Column(Boolean, default=False)

class ObservacionCaseta(Base):
    __tablename__ = "observaciones_caseta"
    id = Column(Integer, primary_key=True, index=True)
    asistencia_id = Column(Integer, ForeignKey("registro_asistencias.id"))
    tipo_observacion = Column(String)
    fecha_registro = Column(DateTime, default=datetime.now(timezone.utc))

class SalidaTemporal(Base):
    __tablename__ = "salidas_temporales"
    id = Column(Integer, primary_key=True, index=True)
    asistencia_id = Column(Integer, ForeignKey("registro_asistencias.id"))
    tipo_salida = Column(Enum(TipoSalidaEnum))
    hora_salida = Column(DateTime, default=datetime.now(timezone.utc))
    hora_regreso = Column(DateTime, nullable=True)
    minutos_descontados = Column(Integer, default=0)
    estado_salida = Column(Enum(EstadoSalidaEnum), default=EstadoSalidaEnum.Abierta)

class FilaExterno(Base):
    __tablename__ = "fila_externos"
    id = Column(Integer, primary_key=True, index=True)
    tipo_visitante = Column(Enum(TipoVisitanteEnum))
    nombre_empresa = Column(String)
    nombre_chofer = Column(String)
    estado_fila = Column(Enum(EstadoFilaEnum), default=EstadoFilaEnum.Espera_Amarillo)
    anden_asignado = Column(String, nullable=True)
    hora_llegada = Column(DateTime, default=datetime.now(timezone.utc))
    hora_entrada = Column(DateTime, nullable=True)
    hora_salida = Column(DateTime, nullable=True)