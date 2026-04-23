@echo off
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

where py >nul 2>nul
if %errorlevel%==0 (
  py "%SCRIPT_DIR%watcher_qt.pyw"
  goto end
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%SCRIPT_DIR%watcher_qt.pyw"
  goto end
)

echo No Python runtime found. Please install Python 3 and PySide6 first.

:end
pause
