# Script đẩy code lên GitHub
# Run: .\push_to_github.ps1 "Commit message"

param(
    [string]$CommitMessage = "Update code"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PUSH TO GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git initialized
if (-Not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    git remote add origin https://github.com/ToanTranDuc/Python.git
}

# Add all files
Write-Host "Adding files..." -ForegroundColor Green
git add .

# Show status
Write-Host ""
Write-Host "Files to commit:" -ForegroundColor Yellow
git status --short

# Commit
Write-Host ""
Write-Host "Committing..." -ForegroundColor Green
git commit -m "$CommitMessage"

# Push
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ DONE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
