"""
build_exe.py – Builds ASAS.exe, ASAS_server.exe and ASAS_cli.exe using PyInstaller.

Usage:
    python build_exe.py

Output:
    dist/ASAS/ASAS.exe         – GUI launcher (double-click to start)
    dist/ASAS/ASAS_server.exe  – Flask web server (called by launcher)
    dist/ASAS/ASAS_cli.exe     – CLI chat       (called by launcher)

Steps performed:
  1. Upgrades pip
  2. Installs/upgrades PyInstaller
  3. Installs all app dependencies (including llama-cpp-python)
  4. Runs PyInstaller with ASAS.spec
  5. Prints the path to the finished EXE
"""

import subprocess
import sys
import os


def run(cmd: list[str], desc: str = "") -> None:
    if desc:
        print(f"\n--- {desc} ---")
    print(f">>> {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\nCommand failed (exit {result.returncode}): {' '.join(cmd)}")
        sys.exit(result.returncode)


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    spec = os.path.join(root, "ASAS.spec")
    reqs = os.path.join(root, "ai_chat", "requirements.txt")

    pip = [sys.executable, "-m", "pip"]

    # 1. Upgrade pip itself
    run(pip + ["install", "--upgrade", "pip"], "שדרוג pip")

    # 2. Ensure PyInstaller is present
    run(pip + ["install", "--upgrade", "pyinstaller"], "התקנת PyInstaller")

    # 3. Install app dependencies (flask, colorama, llama-cpp-python …)
    # Install llama-cpp-python first from the pre-built wheels index to avoid
    # source-build permission errors on Windows (vendor tarball extraction).
    run(
        pip + [
            "install", "--prefer-binary", "--no-cache-dir",
            "llama-cpp-python>=0.2.0",
            "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cpu",
        ],
        "התקנת llama-cpp-python (גרסה מוכנה)",
    )
    run(pip + ["install", "--no-cache-dir", "flask", "colorama"], "התקנת שאר התלויות")

    # 4. Build
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", spec], "בניית EXEs")

    # 5. Report
    exe_path = os.path.join(root, "dist", "ASAS", "ASAS.exe")
    if os.path.isfile(exe_path):
        print(f"\n✅  הבנייה הושלמה!")
        print(f"    תיקיית הפצה: {os.path.join(root, 'dist', 'ASAS')}")
        print("\n    הפץ את תיקיית dist\\ASAS\\ כולה.")
        print("    לחץ פעמיים על ASAS.exe להפעלה – אין צורך ב-Python!")
    else:
        print("\n⚠️  הבנייה הסתיימה אך ASAS.exe לא נמצא.")
        print(f"    בדוק את תיקיית: {os.path.join(root, 'dist')}")


if __name__ == "__main__":
    main()

