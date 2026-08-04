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

## התקנה מהירה

```bash
# 1. שכפל את הפרויקט
git clone https://github.com/g1435r-svg/ASAS.git
cd ASAS

# 2. צור סביבה וירטואלית
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 3. התקן תלויות
pip install -r requirements.txt

# 4. הורד מודל (בחר אחד)
python download_model.py             # Mistral 7B Q4_K_M  (~4.1 GB) – מומלץ
python download_model.py --small     # Llama 1B Q8_0       (~1.3 GB) – קטן ומהיר
```

---

## הפעלה

### ממשק שורת פקודה (CLI)

```bash
python chat_cli.py
```

פקודות בתוך הצ'אט:
| פקודה | תיאור |
|-------|--------|
| `/יציאה` | יציאה מהתוכנה |
| `/היסטוריה` | הצגת היסטוריית שיחה |
| `/נקה` | מחיקת היסטוריה |

### ממשק ווב (דפדפן)

```bash
python app.py
```

פתח בדפדפן: [http://localhost:5000](http://localhost:5000)

---

## שימוש במודל מותאם אישית

```bash
# הגדר נתיב למודל שלך:
MODEL_PATH=/path/to/your/model.gguf python chat_cli.py
MODEL_PATH=/path/to/your/model.gguf python app.py
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
├── app.py              # שרת Flask (ממשק ווב)
├── chat_cli.py         # ממשק שורת פקודה
├── download_model.py   # הורדת מודלים
├── requirements.txt    # תלויות Python
├── templates/
│   └── index.html      # דף HTML לממשק הווב
└── models/             # תיקיית מודלים (ריקה – הורד עם download_model.py)
```

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