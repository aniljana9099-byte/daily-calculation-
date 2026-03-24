@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo   Cash Flow + Extra/Short (2 pages)
echo ========================================
echo.
echo   http://localhost:5000/           — Cash Flow
echo   http://localhost:5000/extra-short — Extra/Short
echo.
echo (Ctrl+C se band)
echo ========================================
start "Cash Flow Server" python app.py
timeout /t 3 /nobreak >nul
start http://localhost:5000/
pause
