@echo off
chcp 65001 >nul
title בניית ASAS.exe
echo ============================================
echo   בניית ASAS.exe – בינה מלאכותית בעברית
echo   אין צורך ב-Python על המחשב של המשתמש!
echo ============================================
echo.

:: Check Python (needed only for building, NOT for running the final EXE)
python --version >nul 2>&1
if errorlevel 1 (
    echo שגיאה: Python לא נמצא על מחשב זה.
    echo Python נדרש רק לבנייה – לא להפעלת ה-EXE הסופי.
    echo הורד Python מ: https://www.python.org/downloads/
    echo.
    echo טיפ: בהתקנת Python – סמן את האפשרות "Add Python to PATH"
    pause
    exit /b 1
)

echo Python נמצא:
python --version
echo.
echo מריץ את סקריפט הבנייה...
echo (זה עשוי לקחת מספר דקות בפעם הראשונה)
echo.

python build_exe.py
if errorlevel 1 (
    echo.
    echo הבנייה נכשלה. ראה הודעות שגיאה למעלה.
    pause
    exit /b 1
)

echo.
if exist "dist\ASAS\ASAS.exe" (
    echo ============================================
    echo   הבנייה הושלמה בהצלחה!
    echo.
    echo   הפץ את תיקיית dist\ASAS\ כולה.
    echo   לחץ פעמיים על ASAS.exe – ללא Python!
    echo ============================================
    start "" "dist\ASAS"
)
pause

