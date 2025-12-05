@echo off
title DFM OSINT Intelligence Pipeline

echo ========================================
echo DFM OSINT Intelligence Pipeline
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo Error: backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Setting up backend...
cd backend

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Failed to install some Python dependencies
    echo Continuing anyway...
)

REM Start backend in background
echo Starting backend server...
start "Backend Server" /min cmd /c "python main.py ^|^| pause"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Go back to root directory
cd ..

REM Start frontend
echo Starting frontend...
start "Frontend Server" cmd /c "npm run dev ^|^| pause"

echo.
echo ========================================
echo System Startup Complete!
echo ========================================
echo Backend API:    http://localhost:8004
echo Frontend UI:    http://localhost:8003
echo.
echo Press any key to close this window...
pause >nul