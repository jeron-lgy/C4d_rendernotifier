@echo off
set SCRIPT_DIR=%~dp0

where pyw >nul 2>nul
if %errorlevel%==0 (
  start "" pyw "%SCRIPT_DIR%configurator.pyw"
  exit /b 0
)

where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw "%SCRIPT_DIR%configurator.pyw"
  exit /b 0
)

where py >nul 2>nul
if %errorlevel%==0 (
  start "" py "%SCRIPT_DIR%configurator.pyw"
  exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
  start "" python "%SCRIPT_DIR%configurator.pyw"
  exit /b 0
)

echo No Python runtime found. Please install Python 3, then run configurator.pyw.
pause
