@echo off
chcp 65001 >nul
title בינה מלאכותית בעברית - שורת פקודה
echo ============================================
echo   בינה מלאכותית בעברית - מצב אופליין
echo   ממשק שורת פקודה
echo ============================================
echo.

if not exist "ai_chat\venv\Scripts\activate.bat" (
    echo שגיאה: הסביבה הוירטואלית לא קיימת.
    echo הרץ קודם: התקנה.bat
    pause
    exit /b 1
)

call ai_chat\venv\Scripts\activate.bat
cd ai_chat
python chat_cli.py
cd ..

pause
