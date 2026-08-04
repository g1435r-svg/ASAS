@echo off
chcp 65001 >nul
title הורדת מודל קטן - Llama 1B
echo ============================================
echo   הורדת מודל Llama 3.2 1B Instruct Q8_0
echo   גודל: ~1.3 GB  |  מהיר וקטן
echo ============================================
echo.

if not exist "ai_chat\venv\Scripts\activate.bat" (
    echo שגיאה: הסביבה הוירטואלית לא קיימת.
    echo הרץ קודם: התקנה.bat
    pause
    exit /b 1
)

call ai_chat\venv\Scripts\activate.bat
python ai_chat\download_model.py --small

echo.
echo לאחר ההורדה הרץ: הפעל_CLI.bat  או  הפעל_WEB.bat
pause
