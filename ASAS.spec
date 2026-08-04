# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for ASAS – Offline Hebrew AI Chat.

Produces THREE executables inside dist/ASAS/:
  ASAS.exe        – GUI launcher (no console, entry-point for end-users)
  ASAS_server.exe – Flask web server
  ASAS_cli.exe    – CLI chat (console window)

All three share the same collected binaries/data so the total folder size is
not multiplied. No Python installation is required on the target machine.

Build with:
    pyinstaller ASAS.spec
or use:
    build.bat  (Windows one-click)
    python build_exe.py
"""

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# ---------------------------------------------------------------------------
# Shared data files
# ---------------------------------------------------------------------------
flask_datas = collect_data_files("flask")
jinja_datas = collect_data_files("jinja2")

common_datas = flask_datas + jinja_datas + [
    (os.path.join("ai_chat", "templates", "index.html"), "templates"),
]

common_hiddenimports = [
    "flask",
    "flask.templating",
    "jinja2",
    "jinja2.ext",
    "werkzeug",
    "werkzeug.serving",
    "werkzeug.routing",
    "colorama",
    "llama_cpp",
    "llama_cpp.llama",
]

common_excludes = [
    "matplotlib", "numpy", "pandas", "PIL", "cv2",
    "scipy", "IPython", "notebook", "PyQt5", "PyQt6",
]

# ---------------------------------------------------------------------------
# Analysis objects – one per script
# ---------------------------------------------------------------------------
a_launcher = Analysis(
    [os.path.join("ai_chat", "launcher.py")],
    pathex=["."],
    binaries=[],
    datas=common_datas,
    hiddenimports=common_hiddenimports + ["tkinter", "tkinter.ttk", "tkinter.messagebox"],
    hookspath=[],
    runtime_hooks=[],
    excludes=common_excludes,
    cipher=block_cipher,
    noarchive=False,
)

a_server = Analysis(
    [os.path.join("ai_chat", "app.py")],
    pathex=["."],
    binaries=[],
    datas=common_datas,
    hiddenimports=common_hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=common_excludes + ["tkinter"],
    cipher=block_cipher,
    noarchive=False,
)

a_cli = Analysis(
    [os.path.join("ai_chat", "chat_cli.py")],
    pathex=["."],
    binaries=[],
    datas=[],
    hiddenimports=common_hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=common_excludes + ["tkinter", "flask", "jinja2", "werkzeug"],
    cipher=block_cipher,
    noarchive=False,
)

# ---------------------------------------------------------------------------
# Merge shared binaries so they are not duplicated on disk
# ---------------------------------------------------------------------------
MERGE(
    (a_launcher, "ASAS",        "ASAS"),
    (a_server,   "ASAS_server", "ASAS_server"),
    (a_cli,      "ASAS_cli",    "ASAS_cli"),
)

# ---------------------------------------------------------------------------
# PYZ archives
# ---------------------------------------------------------------------------
pyz_launcher = PYZ(a_launcher.pure, a_launcher.zipped_data, cipher=block_cipher)
pyz_server   = PYZ(a_server.pure,   a_server.zipped_data,   cipher=block_cipher)
pyz_cli      = PYZ(a_cli.pure,      a_cli.zipped_data,      cipher=block_cipher)

# ---------------------------------------------------------------------------
# EXE objects
# ---------------------------------------------------------------------------
exe_launcher = EXE(
    pyz_launcher, a_launcher.scripts, [],
    exclude_binaries=True,
    name="ASAS",
    debug=False, strip=False, upx=True,
    console=False,   # GUI – no console window
    icon=None,
)

exe_server = EXE(
    pyz_server, a_server.scripts, [],
    exclude_binaries=True,
    name="ASAS_server",
    debug=False, strip=False, upx=True,
    console=False,   # runs hidden in background
    icon=None,
)

exe_cli = EXE(
    pyz_cli, a_cli.scripts, [],
    exclude_binaries=True,
    name="ASAS_cli",
    debug=False, strip=False, upx=True,
    console=True,    # CLI needs a console window
    icon=None,
)

# ---------------------------------------------------------------------------
# Single COLLECT – all three EXEs share one dist/ASAS/ folder
# ---------------------------------------------------------------------------
coll = COLLECT(
    exe_launcher, a_launcher.binaries, a_launcher.zipfiles, a_launcher.datas,
    exe_server,   a_server.binaries,   a_server.zipfiles,   a_server.datas,
    exe_cli,      a_cli.binaries,      a_cli.zipfiles,      a_cli.datas,
    strip=False, upx=True, upx_exclude=[],
    name="ASAS",
)

