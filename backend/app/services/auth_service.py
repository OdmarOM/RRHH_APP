import hashlib
import secrets
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.usuario import UsuarioSistema

class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera hash de contraseña usando SHA256"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{hash_obj.hex()}"
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica contraseña contra hash"""
        try:
            salt, hash_value = hashed_password.split(':')
            hash_obj = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt.encode(), 100000)
            return hash_obj.hex() == hash_value
        except Exception:
            return False
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(UsuarioSistema).filter(
            UsuarioSistema.username == username,
            UsuarioSistema.activo == True
        ).first()
        
        if not user or not AuthService.verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
