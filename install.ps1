# Vibecode Studio Installation Script (Windows)

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Vibecode Studio Installation        ║" -ForegroundColor Cyan
Write-Host "║   Your AI Development Team in a Box    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $versionMatch = [regex]::Match($pythonVersion, "(\d+)\.(\d+)")
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "❌ Error: Python 3.8 or higher required" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Python version OK" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create .vibecode directory if it doesn't exist
if (-not (Test-Path ".vibecode")) {
    Write-Host "Creating .vibecode directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path ".vibecode" | Out-Null
    New-Item -ItemType Directory -Path ".vibecode\sessions" | Out-Null
    Write-Host "✅ .vibecode directory created" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Installation Complete! 🎉            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start Vibecode Studio:" -ForegroundColor Yellow
Write-Host "  1. Activate virtual environment: .\venv\Scripts\Activate.ps1"
Write-Host "  2. Run: python vibecode_studio.py"
Write-Host ""
Write-Host "Or use the quick start:" -ForegroundColor Yellow
Write-Host "  .\run.ps1"
Write-Host ""
