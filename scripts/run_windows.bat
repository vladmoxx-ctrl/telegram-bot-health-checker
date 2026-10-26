@echo off
setlocal
cd /d "%~dp0\.."
set "PYTHONPATH=%CD%\src;%PYTHONPATH%"
python -m telegram_bot_health_checker --env .env
pause
