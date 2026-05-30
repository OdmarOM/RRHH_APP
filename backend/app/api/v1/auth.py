from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.models.usuario import UsuarioSistema
from app.models.rol import Rol
from jose import JWTError, jwt
from app.core.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    rol: str
    empleado_nombre: str | None = None

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    access_token = AuthService.create_access_token(data={"sub": user.username})
    
    empleado_nombre = None
    if user.empleado:
        empleado_nombre = user.empleado.nombre_completo
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        rol=user.rol.nombre,
        empleado_nombre=empleado_nombre
    )

@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido o expirado")
    
    user = db.query(UsuarioSistema).filter(UsuarioSistema.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": user.id,
        "username": user.username,
        "rol": user.rol.nombre,
        "empleado_nombre": user.empleado.nombre_completo if user.empleado else None
    }
