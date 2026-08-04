@echo off
chcp 65001 >nul
title בניית ASAS.exe
echo ============================================
echo   בניית ASAS.exe – בינה מלאכותית בעברית
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

echo מריץ את סקריפט הבנייה...
python build_exe.py

echo.
if exist "dist\ASAS\ASAS.exe" (
    echo ============================================
    echo   הבנייה הושלמה!
    echo   הקובץ נמצא ב: dist\ASAS\ASAS.exe
    echo   הפץ את תיקיית dist\ASAS\ כולה.
    echo ============================================
    start "" "dist\ASAS"
) else (
    echo הבנייה נכשלה. ראה הודעות שגיאה למעלה.
)
pause
