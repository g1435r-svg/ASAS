@echo off
chcp 65001 >nul
title התקנת בינה מלאכותית בעברית
echo ============================================
echo   התקנת תלויות - בינה מלאכותית בעברית
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo שגיאה: Python לא מותקן או לא נמצא ב-PATH.
    echo הורד Python מ: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python נמצא:
python --version
echo.

:: Create venv if needed
if not exist "ai_chat\venv\" (
    echo יוצר סביבה וירטואלית...
    python -m venv ai_chat\venv
)

echo מפעיל סביבה וירטואלית...
call ai_chat\venv\Scripts\activate.bat

echo מתקין תלויות...
echo   שלב 1: מתקין llama-cpp-python (גרסה מוכנה - ללא קומפילציה)...
pip install --prefer-binary --no-cache-dir "llama-cpp-python>=0.2.0" --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
echo   שלב 2: מתקין שאר התלויות...
pip install --no-cache-dir flask colorama

echo.
echo ============================================
echo   ההתקנה הושלמה בהצלחה!
echo   עכשיו הרץ: הורד_מודל.bat
echo ============================================
pause
