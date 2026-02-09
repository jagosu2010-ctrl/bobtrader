@echo off
:: No setlocal here to ensure environment changes are visible in this window
title PowerTrader DEBUG MODE

:: Move to project root
cd /d "D:\Production\PowerTrader_AI"
echo [DEBUG] Current directory: %CD%

:: 1. CLEANUP
echo [STEP 1] Cleaning cache...
if exist "__pycache__" (
    rd /s /q "__pycache__" >nul 2>&1
    echo [OK] Cache cleared.
)
pause

:: 2. ACTIVATION
echo [STEP 2] Activating Virtual Environment...
if not exist ".venv\Scripts\activate.bat" goto :err_venv
call ".venv\Scripts\activate.bat"
echo [OK] Environment activated.
pause

:: 3. DEPENDENCY CHECK
echo [STEP 3] Verifying Python and SDK...
where python
python -c "import kucoin_universal_sdk; print('SDK Import: SUCCESS')"
if %errorlevel% neq 0 goto :err_sdk
pause

:: 4. LAUNCH HUB
echo [STEP 4] Launching Hub...
:: We run python directly (no 'start') to capture errors in this window
python pt_hub.py

if %errorlevel% neq 0 (
    echo.
    echo [CRASH] Hub exited with code %errorlevel%
    echo [CHECK] Did you update pt_hub.py line 16 to ["coins"]?
)
pause
exit /b

:err_venv
echo [ERROR] .venv folder is missing in %CD%
pause
exit /b

:err_sdk
echo [ERROR] Python failed to import SDK. Check .venv installation.
pause
exit /b