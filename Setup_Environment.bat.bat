@echo off
title PowerTrader AI - Environment Setup & Repair
cd /d "D:\Production\PowerTrader_AI"

echo ==================================================
echo      PowerTrader AI: Environment Repair
echo ==================================================
echo.

:: 1. Create/Verify Virtual Environment
echo [1/4] Initializing Virtual Environment (.venv)...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Ensure Python is installed and in your PATH.
    pause
    exit /b
)

:: 2. Activate Environment
echo [2/4] Activating Environment...
call .\.venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate .venv.
    pause
    exit /b
)

:: 3. Upgrade Pip
echo [3/4] Upgrading Pip...
python -m pip install --upgrade pip

:: 4. Install Requirements
echo [4/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b
)

echo.
echo ==================================================
echo      SETUP COMPLETE: Environment is ready.
echo ==================================================
echo You can now run Launch_PowerTrader.bat
pause