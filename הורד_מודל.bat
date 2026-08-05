@echo off
chcp 65001 >nul
title הורדת מודל - Mistral 7B (מומלץ)
echo ============================================
echo   הורדת מודל Mistral 7B Instruct Q4_K_M
echo   גודל: ~4.1 GB  |  איכות: מעולה
echo ============================================
echo.

if not exist "ai_chat\venv\Scripts\activate.bat" (
    echo שגיאה: הסביבה הוירטואלית לא קיימת.
    echo הרץ קודם: התקנה.bat
    pause
    exit /b 1
)

call ai_chat\venv\Scripts\activate.bat
python ai_chat\download_model.py

echo.
echo לאחר ההורדה הרץ: הפעל_CLI.bat  או  הפעל_WEB.bat
pause
