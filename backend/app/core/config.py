# Configuración simple sin pydantic_settings
import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hr_vigilance.db")
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

settings = Settings()
