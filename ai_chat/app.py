"""
Web UI for offline Hebrew AI Chat.
Run with:  python app.py
Then open:  http://localhost:5000
"""

import os
import datetime
import json

from flask import Flask, render_template, request, jsonify, session

try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.urandom(24)

SYSTEM_PROMPT = (
    "You are a helpful AI assistant that speaks Hebrew fluently. "
    "Always respond in Hebrew unless the user explicitly writes in another language. "
    "Be friendly, accurate, and concise."
)

_llm: Llama | None = None


def get_llm() -> "Llama | None":
    global _llm
    if _llm is not None:
        return _llm
    if not LLAMA_AVAILABLE:
        return None
    model_path = os.environ.get("MODEL_PATH", "")
    if not model_path:
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        if os.path.isdir(models_dir):
            for fname in os.listdir(models_dir):
                if fname.endswith(".gguf"):
                    model_path = os.path.join(models_dir, fname)
                    break
    if not model_path or not os.path.isfile(model_path):
        return None
    _llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=os.cpu_count() or 4,
        verbose=False,
    )
    return _llm


def build_prompt(history: list, user_message: str) -> str:
    prompt = f"<<SYS>>\n{SYSTEM_PROMPT}\n<</SYS>>\n\n"
    for turn in history[-10:]:
        prompt += f"[INST] {turn['user']} [/INST] {turn['assistant']}\n"
    prompt += f"[INST] {user_message} [/INST]"
    return prompt


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "הודעה ריקה"}), 400

    history = session.get("history", [])

    llm = get_llm()
    if llm is None:
        return jsonify({
            "error": (
                "המודל אינו זמין. "
                "הנח קובץ GGUF בתיקיית models/ והפעל מחדש."
            )
        }), 503

    prompt = build_prompt(history, user_message)
    try:
        output = llm(
            prompt,
            max_tokens=1024,
            stop=["[INST]", "</s>"],
            echo=False,
        )
        reply = output["choices"][0]["text"].strip()
    except Exception:  # noqa: BLE001
        app.logger.exception("Error generating response")
        return jsonify({"error": "שגיאה פנימית בעת יצירת תגובה"}), 500

    history.append({
        "user": user_message,
        "assistant": reply,
        "timestamp": datetime.datetime.now().isoformat(),
    })
    session["history"] = history

    return jsonify({"reply": reply})


@app.route("/api/history")
def get_history():
    return jsonify(session.get("history", []))


@app.route("/api/clear", methods=["POST"])
def clear_history():
    session["history"] = []
    return jsonify({"ok": True})


@app.route("/api/status")
def status():
    llm = get_llm()
    return jsonify({
        "model_loaded": llm is not None,
        "llama_available": LLAMA_AVAILABLE,
    })


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
