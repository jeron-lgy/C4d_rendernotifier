@echo off
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%\.."

where py >nul 2>nul
if %errorlevel% neq 0 (
  echo Python launcher "py" not found.
  pause
  exit /b 1
)

py -m pip install -r watcher\requirements-web-console.txt pyinstaller
if %errorlevel% neq 0 (
  echo Failed to install packaging dependencies.
  pause
  exit /b 1
)

py -m PyInstaller --noconfirm --clean watcher\web_console.spec
if %errorlevel% neq 0 (
  echo Build failed.
  pause
  exit /b 1
)

echo.
echo Build complete.
echo Output:
echo %cd%\dist\TongzhiWatcher.exe
pause
