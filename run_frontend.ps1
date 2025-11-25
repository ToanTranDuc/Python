# PowerShell script để khởi động frontend
# Sử dụng: .\run_frontend.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IMAGE CAPTIONING - FRONTEND" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend
Set-Location frontend

Write-Host "[INFO] Starting frontend server..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Frontend available at:" -ForegroundColor Cyan
Write-Host "  http://localhost:5500" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start simple HTTP server
python -m http.server 5500
