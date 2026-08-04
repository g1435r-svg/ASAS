@echo off
chcp 65001 >nul
title התקנה מלאה - בינה מלאכותית בעברית

echo ============================================
echo   התקנה מלאה - בינה מלאכותית בעברית
echo   צעד אחד - הכל אוטומטי!
echo ============================================
echo.

:: ── 1. Check Python ────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo שגיאה: Python לא מותקן או לא נמצא ב-PATH.
    echo הורד Python מ: https://www.python.org/downloads/
    echo.
    echo טיפ: בהתקנת Python - סמן "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/5] Python נמצא:
python --version
echo.

:: ── 2. Create venv ─────────────────────────────────────────────────────────
echo [2/5] מכין סביבה וירטואלית...
if not exist "ai_chat\venv\" (
    python -m venv ai_chat\venv
    if errorlevel 1 (
        echo שגיאה: יצירת הסביבה הוירטואלית נכשלה.
        pause
        exit /b 1
    )
)
call ai_chat\venv\Scripts\activate.bat
echo       הסביבה הוירטואלית מוכנה.
echo.

:: ── 3. Install dependencies ────────────────────────────────────────────────
echo [3/5] מתקין תלויות (זה עשוי לקחת מספר דקות)...
echo       שלב 1: מתקין llama-cpp-python (גרסה מוכנה - ללא קומפילציה)...
pip install --prefer-binary --no-cache-dir "llama-cpp-python>=0.2.0" --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
if errorlevel 1 (
    echo.
    echo שגיאה: התקנת llama-cpp-python נכשלה.
    pause
    exit /b 1
)
echo       שלב 2: מתקין שאר התלויות...
pip install --no-cache-dir flask colorama
if errorlevel 1 (
    echo.
    echo שגיאה: התקנת התלויות נכשלה.
    pause
    exit /b 1
)
echo       התלויות הותקנו בהצלחה.
echo.

:: ── 4. Choose model ────────────────────────────────────────────────────────
echo [4/5] בחר מודל להורדה:
echo.
echo   1. Mistral 7B Instruct Q4_K_M  (~4.1 GB) - מומלץ, איכות גבוהה
echo   2. Llama 3.2 1B Instruct Q8_0  (~1.3 GB) - קטן ומהיר
echo.

:choose_model
set /p MODEL_CHOICE="הזן 1 או 2 ואז Enter: "

if "%MODEL_CHOICE%"=="1" (
    set MODEL_FLAG=
    echo.
    echo מוריד מודל Mistral 7B...
    goto download_model
)
if "%MODEL_CHOICE%"=="2" (
    set MODEL_FLAG=--small
    echo.
    echo מוריד מודל Llama 1B...
    goto download_model
)

echo בחירה לא חוקית. הזן 1 או 2.
goto choose_model

:download_model
python ai_chat\download_model.py %MODEL_FLAG%
if errorlevel 1 (
    echo.
    echo שגיאה: הורדת המודל נכשלה.
    echo בדוק את חיבור האינטרנט ונסה שוב.
    pause
    exit /b 1
)
echo.

:: ── 5. Launch ──────────────────────────────────────────────────────────────
echo [5/5] ההתקנה הושלמה בהצלחה!
echo.
echo ============================================
echo   הכל מוכן! איך תרצה להפעיל?
echo ============================================
echo.
echo   1. ממשק ווב  (http://localhost:5000)
echo   2. שורת פקודה (CLI)
echo   3. סיום (הפעל מאוחר יותר עם הפעל_WEB.bat / הפעל_CLI.bat)
echo.

:choose_launch
set /p LAUNCH_CHOICE="הזן 1, 2 או 3 ואז Enter: "

if "%LAUNCH_CHOICE%"=="1" goto launch_web
if "%LAUNCH_CHOICE%"=="2" goto launch_cli
if "%LAUNCH_CHOICE%"=="3" goto done

echo בחירה לא חוקית. הזן 1, 2 או 3.
goto choose_launch

:launch_web
echo.
echo מפעיל ממשק ווב...
echo פתח בדפדפן: http://localhost:5000
echo לעצור: Ctrl+C
echo.
start "" cmd /c "timeout /t 2 >nul && start http://localhost:5000"
cd ai_chat
python app.py
cd ..
goto done

:launch_cli
echo.
echo מפעיל שורת פקודה...
echo.
cd ai_chat
python chat_cli.py
cd ..
goto done

:done
echo.
echo להפעלה מחדש בעתיד:
echo   הפעל_WEB.bat  - ממשק ווב
echo   הפעל_CLI.bat  - שורת פקודה
echo.
pause
