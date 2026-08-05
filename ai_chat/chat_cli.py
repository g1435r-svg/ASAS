"""
Offline Hebrew AI Chat - CLI interface
Uses llama-cpp-python to run GGUF models locally, fully offline.
"""

import sys
import os
import json
import datetime

try:
    from llama_cpp import Llama
except ImportError:
    print("שגיאה: llama-cpp-python לא מותקן.")
    print("הרץ:  pip install llama-cpp-python")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

HISTORY_FILE = "chat_history.json"

SYSTEM_PROMPT = (
    "You are a helpful AI assistant that speaks Hebrew fluently. "
    "Always respond in Hebrew unless the user explicitly writes in another language. "
    "Be friendly, accurate, and concise."
)


def color(text: str, fore: str = "") -> str:
    if HAS_COLOR and fore:
        return fore + text + Style.RESET_ALL
    return text


def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_history(history: list) -> None:
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def build_prompt(history: list, user_message: str) -> str:
    """Build a simple instruction-style prompt from conversation history."""
    prompt = f"<<SYS>>\n{SYSTEM_PROMPT}\n<</SYS>>\n\n"
    for turn in history[-10:]:          # keep last 10 turns to limit context
        prompt += f"[INST] {turn['user']} [/INST] {turn['assistant']}\n"
    prompt += f"[INST] {user_message} [/INST]"
    return prompt


def find_model() -> str:
    """Return path to first .gguf file found in ./models directory."""
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    if not os.path.isdir(models_dir):
        return ""
    for fname in os.listdir(models_dir):
        if fname.endswith(".gguf"):
            return os.path.join(models_dir, fname)
    return ""


def main() -> None:
    print(color("=" * 60, Fore.CYAN if HAS_COLOR else ""))
    print(color("  בינה מלאכותית בעברית - מצב אופליין", Fore.CYAN if HAS_COLOR else ""))
    print(color("=" * 60, Fore.CYAN if HAS_COLOR else ""))

    # Determine model path
    model_path = os.environ.get("MODEL_PATH", "")
    if not model_path:
        model_path = find_model()
    if not model_path or not os.path.isfile(model_path):
        print(color("\nשגיאה: לא נמצא מודל.", Fore.RED if HAS_COLOR else ""))
        print("הורד מודל GGUF (ראה download_model.py) והנח אותו בתיקיית models/")
        print("או הגדר את משתנה הסביבה MODEL_PATH לנתיב המודל.")
        sys.exit(1)

    print(f"\nטוען מודל: {os.path.basename(model_path)}")
    print("אנא המתן...\n")

    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=os.cpu_count() or 4,
        verbose=False,
    )

    history = load_history()
    print(color("המודל מוכן! הקלד את שאלתך בעברית. לצאת: /יציאה או /exit\n",
                Fore.GREEN if HAS_COLOR else ""))

    while True:
        try:
            user_input = input(color("אתה: ", Fore.YELLOW if HAS_COLOR else "")).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nלהתראות!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/exit", "/יציאה", "exit", "quit"):
            print("להתראות!")
            break

        if user_input == "/היסטוריה":
            for i, turn in enumerate(history, 1):
                print(f"\n--- שיחה {i} ---")
                print(f"אתה: {turn['user']}")
                print(f"בינה: {turn['assistant']}")
            continue

        if user_input == "/נקה":
            history = []
            save_history(history)
            print("ההיסטוריה נמחקה.")
            continue

        prompt = build_prompt(history, user_input)

        print(color("בינה: ", Fore.GREEN if HAS_COLOR else ""), end="", flush=True)
        try:
            output = llm(
                prompt,
                max_tokens=1024,
                stop=["[INST]", "</s>"],
                echo=False,
            )
            reply = output["choices"][0]["text"].strip()
        except Exception as exc:  # noqa: BLE001
            reply = f"שגיאה בעת יצירת תגובה: {exc}"

        print(reply)
        print()

        history.append({
            "user": user_input,
            "assistant": reply,
            "timestamp": datetime.datetime.now().isoformat(),
        })
        save_history(history)


if __name__ == "__main__":
    main()
