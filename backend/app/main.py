from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.v1 import caseta, auth, supervisor

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema RRHH y Vigilancia")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(caseta.router, prefix="/api/v1/caseta", tags=["Caseta"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(supervisor.router, tags=["Supervisor"])
app.include_router(supervisor.router2, tags=["RRHH"])

@app.get("/")
async def root():
    return {"message": "Sistema RRHH y Vigilancia API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
