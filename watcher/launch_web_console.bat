@echo off
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -like '*web_console.pyw*' -or $_.CommandLine -like '*web_console.py*') -and $_.ProcessId -ne $PID } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>nul

where pyw >nul 2>nul
if %errorlevel%==0 (
  start "" pyw "%SCRIPT_DIR%web_console.pyw"
  exit /b 0
)

where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw "%SCRIPT_DIR%web_console.pyw"
  exit /b 0
)

where py >nul 2>nul
if %errorlevel%==0 (
  start "" py "%SCRIPT_DIR%web_console.pyw"
  exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
  start "" python "%SCRIPT_DIR%web_console.pyw"
  exit /b 0
)

echo No Python runtime found. Please install Python 3 first.
pause
