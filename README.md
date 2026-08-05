# ASAS – בינה מלאכותית בעברית, מצב אופליין

תוכנה לשיחה עם בינה מלאכותית בעברית, **ללא צורך באינטרנט**, באמצעות מודלים מקומיים (GGUF).

---

## דרישות מערכת

| פריט | מינימום |
|------|---------|
| Python | 3.10+ |
| RAM | 8 GB (16 GB מומלץ) |
| אחסון | 5–8 GB לקובץ המודל |
| מעבד | x86-64 (תמיכת GPU אופציונלית) |

---

## התקנה והפעלה (Windows – קל מאוד!)

פשוט לחץ פעמיים על הקבצים הבאים לפי הסדר:

| קובץ BAT | מה הוא עושה |
|----------|-------------|
| `התקנה.bat` | מתקין Python ותלויות אוטומטית |
| `הורד_מודל.bat` | מוריד מודל Mistral 7B (~4.1 GB) – **מומלץ** |
| `הורד_מודל_קטן.bat` | מוריד מודל Llama 1B (~1.3 GB) – מהיר יותר |
| `הפעל_CLI.bat` | פותח צ'אט בעברית בשורת פקודה |
| `הפעל_WEB.bat` | פותח ממשק ווב ופותח דפדפן אוטומטית |

---

## התקנה ידנית (Linux / macOS)

```bash
# 1. שכפל את הפרויקט
git clone https://github.com/g1435r-svg/ASAS.git
cd ASAS

# 2. צור סביבה וירטואלית
python -m venv ai_chat/venv
source ai_chat/venv/bin/activate

# 3. התקן תלויות
pip install -r ai_chat/requirements.txt

# 4. הורד מודל (בחר אחד)
python ai_chat/download_model.py             # Mistral 7B Q4_K_M  (~4.1 GB) – מומלץ
python ai_chat/download_model.py --small     # Llama 1B Q8_0       (~1.3 GB) – קטן ומהיר
```

---

## הפעלה ידנית

### ממשק שורת פקודה (CLI)

```bash
cd ai_chat && python chat_cli.py
```

פקודות בתוך הצ'אט:
| פקודה | תיאור |
|-------|--------|
| `/יציאה` | יציאה מהתוכנה |
| `/היסטוריה` | הצגת היסטוריית שיחה |
| `/נקה` | מחיקת היסטוריה |

### ממשק ווב (דפדפן)

```bash
cd ai_chat && python app.py
```

פתח בדפדפן: [http://localhost:5000](http://localhost:5000)

---

## שימוש במודל מותאם אישית

```bash
MODEL_PATH=/path/to/your/model.gguf python ai_chat/chat_cli.py
MODEL_PATH=/path/to/your/model.gguf python ai_chat/app.py
```

---

## מודלים נתמכים

כל מודל בפורמט **GGUF** תואם. מומלץ:

| מודל | גודל | איכות |
|------|------|--------|
| Mistral 7B Instruct Q4_K_M | ~4.1 GB | ⭐⭐⭐⭐ |
| Llama 3.2 1B Instruct Q8_0 | ~1.3 GB | ⭐⭐⭐ |

---

## מבנה הפרויקט

```
ASAS/
├── build.bat               # בנייה חד-לחיצתית של ASAS.exe (Windows)
├── build_exe.py            # סקריפט בנייה (PyInstaller)
├── ASAS.spec               # קובץ הגדרות PyInstaller
├── התקנה.bat               # התקנה ידנית (ללא EXE)
├── הורד_מודל.bat           # הורדת Mistral 7B
├── הורד_מודל_קטן.bat       # הורדת Llama 1B
├── הפעל_CLI.bat            # הפעלת CLI
├── הפעל_WEB.bat            # הפעלת ממשק ווב
└── ai_chat/
    ├── launcher.py         # GUI launcher (כניסה ל-EXE)
    ├── app.py              # שרת Flask
    ├── chat_cli.py         # ממשק שורת פקודה
    ├── download_model.py   # הורדת מודלים
    ├── requirements.txt    # תלויות Python
    ├── templates/
    │   └── index.html      # דף ווב
    └── models/             # תיקיית מודלים (הורד עם launcher)
```

---

## בניית EXE פורטבילי

### Windows – לחיצה אחת

```
build.bat
```

### ידנית

```bash
pip install pyinstaller
pip install -r ai_chat/requirements.txt
pyinstaller --noconfirm ASAS.spec
```

הפלט: `dist/ASAS/ASAS.exe`  
**הפץ את תיקיית `dist/ASAS/` כולה** – לחץ פעמיים על `ASAS.exe`.

בהפעלה ראשונה: חלון גרפי יופיע, בחר מודל ולחץ **הורד**, ואז התחל לשוחח.

> **הערה:** המודל עצמו (~1–4 GB) מוריד בנפרד – לא ניתן לכלול אותו בתוך EXE.

---

## שאלות נפוצות

**ש: האם זה עובד ללא אינטרנט?**  
כן! לאחר הורדת המודל, כל הפעולות מקומיות לחלוטין.

**ש: האם יש תמיכת GPU?**  
כן, בהתקנה ייעודית:
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

**ש: המודל לא מגיב בעברית?**  
ודא שהמודל שבחרת תומך בעברית. Mistral 7B Instruct מגיב בעברית היטב.