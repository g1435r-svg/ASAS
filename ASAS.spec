# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for ASAS – Offline Hebrew AI Chat.

Build with:
    pyinstaller ASAS.spec
or use:
    build.bat  (Windows one-click)
    python build_exe.py
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect Flask templates and static files
flask_datas = collect_data_files("flask")

# ai_chat source tree
ai_chat_datas = [
    (os.path.join("ai_chat", "templates", "index.html"), os.path.join("templates")),
    (os.path.join("ai_chat", "app.py"),         "."),
    (os.path.join("ai_chat", "chat_cli.py"),    "."),
    (os.path.join("ai_chat", "download_model.py"), "."),
]

all_datas = flask_datas + ai_chat_datas

a = Analysis(
    [os.path.join("ai_chat", "launcher.py")],
    pathex=["."],
    binaries=[],
    datas=all_datas,
    hiddenimports=[
        "tkinter",
        "tkinter.ttk",
        "tkinter.messagebox",
        "flask",
        "flask.templating",
        "jinja2",
        "werkzeug",
        "colorama",
        # llama_cpp is loaded at runtime; mark as optional hidden import
        "llama_cpp",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "numpy",
        "pandas",
        "PIL",
        "cv2",
        "scipy",
        "IPython",
        "notebook",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ASAS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # no console window – launcher is a GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # replace with "ai_chat/icon.ico" if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ASAS",
)
