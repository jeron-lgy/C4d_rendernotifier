# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


ROOT = Path.cwd()
WATCHER_DIR = ROOT / "watcher"
PLUGIN_DIR = ROOT / "c4d_render_notifier"

datas = [
    (str(WATCHER_DIR / "web"), "web"),
    (str(PLUGIN_DIR), "c4d_render_notifier"),
]

hiddenimports = [
    "pystray",
    "PIL",
    "PIL.Image",
    "PIL.ImageDraw",
]


a = Analysis(
    [str(WATCHER_DIR / "web_console.pyw")],
    pathex=[str(WATCHER_DIR), str(PLUGIN_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="TongzhiWatcher",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
