@echo off
setlocal
cd /d "%~dp0\.."
python -m telegram_bot_health_checker --env .env
pause
