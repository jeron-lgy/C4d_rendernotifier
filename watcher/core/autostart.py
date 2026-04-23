import os


AUTOSTART_FILE_NAME = "TongzhiWatcher.cmd"


def _startup_dir():
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return ""
    return os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")


def get_autostart_path():
    startup_dir = _startup_dir()
    if not startup_dir:
        return ""
    return os.path.join(startup_dir, AUTOSTART_FILE_NAME)


def is_enabled():
    path = get_autostart_path()
    return bool(path and os.path.exists(path))


def enable(watcher_ui_script_path):
    startup_dir = _startup_dir()
    if not startup_dir:
        raise RuntimeError("APPDATA is not available.")
    if not os.path.exists(startup_dir):
        os.makedirs(startup_dir)

    launcher_path = get_autostart_path()
    script_dir = os.path.dirname(watcher_ui_script_path)
    content = (
        "@echo off\n"
        "cd /d \"{0}\"\n"
        "where pyw >nul 2>nul\n"
        "if %errorlevel%==0 start \"\" pyw \"{1}\"\n"
        "if %errorlevel%==0 exit /b 0\n"
        "where pythonw >nul 2>nul\n"
        "if %errorlevel%==0 start \"\" pythonw \"{1}\"\n"
        "if %errorlevel%==0 exit /b 0\n"
        "where py >nul 2>nul\n"
        "if %errorlevel%==0 start \"\" py \"{1}\"\n"
        "if %errorlevel%==0 exit /b 0\n"
        "where python >nul 2>nul\n"
        "if %errorlevel%==0 start \"\" python \"{1}\"\n"
    ).format(script_dir, watcher_ui_script_path)
    with open(launcher_path, "w", encoding="utf-8") as handle:
        handle.write(content)


def disable():
    path = get_autostart_path()
    if path and os.path.exists(path):
        os.remove(path)
