from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Crea las tablas en la base de datos automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de RRHH y Vigilancia")

@app.get("/")
def leer_raiz():
    return {"mensaje": "API del Sistema de Vigilancia en línea y funcionando."}

@app.get("/api/v1/departamentos")
def obtener_departamentos(db: Session = Depends(get_db)):
    departamentos = db.query(models.Departamento).all()
    return departamentos