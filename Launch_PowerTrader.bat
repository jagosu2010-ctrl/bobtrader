@echo off
setlocal
:: ================================================================================
:: POWERTRADER AI MASTER LAUNCHER - HARDENED VERSION
:: ================================================================================

set "POWERTRADER_SYSTEM_DEBUG_MODE=True"
title PowerTrader AI [WATCHDOG ACTIVE]

:: Move to project root
cd /d "D:\Production\PowerTrader_AI"

echo ============================================
echo      PowerTrader AI: System Startup
echo ============================================

:: 1. CLEANUP: Safe cache and process management
echo [1/6] Cleaning environment...
if exist "__pycache__" (
    rd /s /q "__pycache__" >nul 2>&1
)
taskkill /F /IM python.exe /T >nul 2>&1

:: 2. VIRTUAL ENVIRONMENT: Jump logic to avoid IF-block crashes
echo [2/6] Activating Virtual Environment...
if not exist ".venv\Scripts\activate.bat" goto :no_venv
call ".venv\Scripts\activate.bat"
goto :venv_ok

:no_venv
echo [ERROR] Virtual environment (.venv) not found!
pause
exit /b

:venv_ok
:: 3. PRE-FLIGHT: Verify critical exchange SDK
echo [3/6] Verifying Dependencies...
python -c "import kucoin_universal_sdk" >nul 2>&1
if %errorlevel% neq 0 goto :no_sdk
goto :sdk_ok

:no_sdk
echo [ERROR] KuCoin Universal SDK not found in .venv!
echo Run Setup_Environment.bat first.
pause
exit /b

:sdk_ok
:: 4. NEURAL ENGINE: Start background thinker
echo [4/6] Starting Neural Engine (Thinker)...
start "PT Neural Engine" cmd /k "python pt_thinker.py"

:: 5. READY-GATE: Wait for BTC folder initialization
echo [5/6] Waiting for BTC Subdirectory Readiness...
:wait_ready
timeout /t 2 /nobreak >nul
if not exist "BTC\runner_ready.json" goto wait_ready
echo [READY] Neural Engine signaled OK.

:: 6. HUB WATCHDOG: Persistent loop for the Main Hub
echo [6/6] Launching Main Dashboard with Watchdog...

:watchdog_start
echo [%time%] Starting Hub Instance...
python pt_hub.py

:: Use GOTO logic for the exit code check to prevent "unexpected at this time"
if %errorlevel% equ 0 goto :session_end
goto :hub_crash

:hub_crash
echo [%time%] Hub crashed with code %errorlevel%.
echo Recovering in 10 seconds...
if exist "__pycache__" (
    rd /s /q "__pycache__" >nul 2>&1
)
timeout /t 10
goto :watchdog_start

:session_end
echo.
echo ============================================
echo      PowerTrader AI: Session Ended Normally
echo ============================================
pause