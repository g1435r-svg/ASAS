@echo off
chcp 65001 >nul
title בינה מלאכותית בעברית - ממשק ווב
echo ============================================
echo   בינה מלאכותית בעברית - מצב אופליין
echo   ממשק ווב - http://localhost:5000
echo ============================================
echo.

if not exist "ai_chat\venv\Scripts\activate.bat" (
    echo שגיאה: הסביבה הוירטואלית לא קיימת.
    echo הרץ קודם: התקנה.bat
    pause
    exit /b 1
)

call ai_chat\venv\Scripts\activate.bat

echo מפעיל שרת...
echo פתח בדפדפן: http://localhost:5000
echo לעצור: Ctrl+C
echo.

:: Open browser after 2 seconds
start "" cmd /c "timeout /t 2 >nul && start http://localhost:5000"

cd ai_chat
python app.py
cd ..

pause
