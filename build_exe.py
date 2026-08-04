"""
build_exe.py – Builds ASAS.exe using PyInstaller.

Usage:
    python build_exe.py

Output:
    dist/ASAS/ASAS.exe  (plus supporting files in dist/ASAS/)

Steps performed:
  1. Installs/upgrades PyInstaller if missing
  2. Runs PyInstaller with ASAS.spec
  3. Prints the path to the finished EXE
"""

import subprocess
import sys
import os


def run(cmd: list[str]) -> None:
    print(f"\n>>> {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\nCommand failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    spec = os.path.join(root, "ASAS.spec")

    # 1. Ensure PyInstaller is available
    try:
        import PyInstaller  # noqa: F401
        print("PyInstaller כבר מותקן.")
    except ImportError:
        print("מתקין PyInstaller...")
        run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Also ensure app dependencies are installed (needed at build time)
    reqs = os.path.join(root, "ai_chat", "requirements.txt")
    run([sys.executable, "-m", "pip", "install", "-r", reqs])

    # 3. Run PyInstaller
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", spec])

    exe_path = os.path.join(root, "dist", "ASAS", "ASAS.exe")
    if os.path.isfile(exe_path):
        print(f"\n✅  הבנייה הושלמה:\n    {exe_path}")
        print("\nהפץ את תיקיית dist/ASAS/ כולה למשתמשים.")
        print("לחץ פעמיים על ASAS.exe להפעלה.")
    else:
        print("\n⚠️  הבנייה הסתיימה אך לא נמצא EXE בנתיב הצפוי.")
        print(f"    חפש ב: {os.path.join(root, 'dist')}")


if __name__ == "__main__":
    main()
