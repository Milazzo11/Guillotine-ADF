@echo off
echo [TEST] Attempting to kill service.py and watchdog.exe...

REM Kill the Python service process
taskkill /F /IM python.exe /FI "WINDOWTITLE eq service.py*" >nul 2>&1

REM Kill any watchdog.exe instances
taskkill /F /IM watchdog.exe >nul 2>&1

echo [TEST] Kill attempt complete.
