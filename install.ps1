# install.ps1 - Script de instalación para Windows
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalando Sistema RRHH y Vigilancia" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Verificar Python
Write-Host "`n✓ Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "  $pythonVersion detectado" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python no encontrado. Instalar Python 3.12" -ForegroundColor Red
    exit 1
}

# Verificar Node.js
Write-Host "`n✓ Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  Node.js $nodeVersion detectado" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Node.js no encontrado" -ForegroundColor Red
    exit 1
}

# Instalar dependencias backend
Write-Host "`n✓ Instalando dependencias del Backend..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt

# Inicializar base de datos
Write-Host "`n✓ Inicializando base de datos..." -ForegroundColor Yellow
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine); print('Base de datos creada')"

# Instalar dependencias frontend
Write-Host "`n✓ Instalando dependencias del Frontend..." -ForegroundColor Yellow
Set-Location ../frontend
npm install

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nPara iniciar el sistema:" -ForegroundColor Yellow
Write-Host "1. Backend: cd backend && python run.py" -ForegroundColor White
Write-Host "2. Frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host "`nAccede a: http://localhost:5173" -ForegroundColor Cyan