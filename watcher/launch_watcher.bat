@echo off
set SCRIPT_DIR=%~dp0

where py >nul 2>nul
if %errorlevel%==0 (
  py "%SCRIPT_DIR%app.py"
  exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%SCRIPT_DIR%app.py"
  exit /b 0
)

echo No Python runtime found. Please install Python 3 first.
pause

