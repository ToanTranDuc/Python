# Script chạy cả Backend + Frontend cùng lúc
Write-Host "🚀 Starting Image Captioning App..." -ForegroundColor Cyan
Write-Host ""

# Kiểm tra dependencies
$hasFastAPI = python -c "import fastapi" 2>$null
if (-not $?) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install fastapi uvicorn python-multipart
}

# Start Backend in background
Write-Host "✓ Starting Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python main.py"

# Wait a bit
Start-Sleep -Seconds 2

# Start Frontend in background
Write-Host "✓ Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; python -m http.server 5500"

# Wait a bit more
Start-Sleep -Seconds 2

# Open browser
Write-Host "✓ Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:5500"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ App is running!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:5500" -ForegroundColor Yellow
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Close the PowerShell windows to stop" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
