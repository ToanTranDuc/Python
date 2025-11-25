# PowerShell script để khởi động backend server
# Sử dụng: .\run_backend.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IMAGE CAPTIONING - BACKEND SERVER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "[WARNING] Virtual environment not found!" -ForegroundColor Yellow
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    Write-Host ""
}

# Check if requirements are installed
Write-Host "[INFO] Checking dependencies..." -ForegroundColor Green
$installed = pip list 2>$null | Select-String "fastapi"
if (-not $installed) {
    Write-Host "[WARNING] Dependencies not installed!" -ForegroundColor Yellow
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Navigate to backend
Write-Host "[INFO] Starting backend server..." -ForegroundColor Green

# Check mode
if (-Not (Test-Path "..\models\best_model_captioning.h5")) {
    Write-Host ""
    Write-Host "⚠️  DEMO MODE - No model files" -ForegroundColor Yellow
    Write-Host "   Using mock captions for testing UI" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✓ Model files found - Production mode" -ForegroundColor Green
}

Set-Location backend

# Start server
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Server starting at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "  API Docs:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python main.py
