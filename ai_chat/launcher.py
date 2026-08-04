"""
ASAS Launcher – graphical entry-point for the offline Hebrew AI chat.

Flow:
  1. Show main window with two buttons: CLI chat / Web UI
  2. If no model is found → offer to download (with a progress bar)
  3. Launch the chosen mode in a subprocess

Built with tkinter only (stdlib) so PyInstaller bundles it with zero extra deps.
"""

from __future__ import annotations

import os
import sys
import subprocess
import threading
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------------------------------------------
# Paths – work whether frozen (EXE) or run as a plain script
# ---------------------------------------------------------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(BASE_DIR, "models")
APP_PY     = os.path.join(BASE_DIR, "app.py")
CLI_PY     = os.path.join(BASE_DIR, "chat_cli.py")

# ---------------------------------------------------------------------------
# Model catalogue
# ---------------------------------------------------------------------------
MODELS = {
    "mistral": {
        "label": "Mistral 7B Instruct Q4_K_M  (~4.1 GB) – מומלץ",
        "name":  "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "url": (
            "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
            "/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        ),
    },
    "llama": {
        "label": "Llama 3.2 1B Instruct Q8_0  (~1.3 GB) – קטן ומהיר",
        "name":  "Llama-3.2-1B-Instruct-Q8_0.gguf",
        "url": (
            "https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
            "/resolve/main/Llama-3.2-1B-Instruct-Q8_0.gguf"
        ),
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_model() -> str:
    """Return path to the first .gguf file found in MODELS_DIR, or ''."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    for fname in os.listdir(MODELS_DIR):
        if fname.endswith(".gguf"):
            return os.path.join(MODELS_DIR, fname)
    return ""


def python_exe() -> str:
    """Return the Python executable to use for sub-processes."""
    if getattr(sys, "frozen", False):
        # When frozen we ship a bundled python; fall back to sys.executable
        bundled = os.path.join(BASE_DIR, "_internal", "python.exe")
        if os.path.isfile(bundled):
            return bundled
        return sys.executable
    return sys.executable


# ---------------------------------------------------------------------------
# Main launcher window
# ---------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ASAS – בינה מלאכותית בעברית")
        self.resizable(False, False)
        self.configure(bg="#0d1117")

        # RTL support hint
        self.option_add("*font", ("Segoe UI", 11))

        self._build_ui()
        self._check_model_on_start()

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        PAD = {"padx": 20, "pady": 10}

        # Title
        tk.Label(
            self, text="🤖  ASAS – בינה מלאכותית בעברית",
            bg="#0d1117", fg="#58a6ff", font=("Segoe UI", 14, "bold"),
        ).pack(**PAD, pady=(20, 4))

        tk.Label(
            self, text="מצב אופליין – ללא צורך באינטרנט לאחר הורדת המודל",
            bg="#0d1117", fg="#8b949e", font=("Segoe UI", 9),
        ).pack(padx=20, pady=(0, 12))

        # Model status
        self.model_var = tk.StringVar(value="בודק מודל...")
        tk.Label(
            self, textvariable=self.model_var,
            bg="#0d1117", fg="#3fb950", font=("Segoe UI", 10),
        ).pack(padx=20, pady=(0, 10))

        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)

        # Launch buttons
        btn_frame = tk.Frame(self, bg="#0d1117")
        btn_frame.pack(**PAD)

        self._btn(btn_frame, "💬  שיחה – שורת פקודה", "#238636", self._launch_cli).pack(
            side="right", padx=6, ipadx=10, ipady=6)
        self._btn(btn_frame, "🌐  שיחה – ממשק ווב",   "#1f6feb", self._launch_web).pack(
            side="right", padx=6, ipadx=10, ipady=6)

        # Download section
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)

        dl_frame = tk.Frame(self, bg="#0d1117")
        dl_frame.pack(padx=20, pady=10)

        tk.Label(dl_frame, text="הורדת מודל:", bg="#0d1117", fg="#c9d1d9").pack(
            side="right", padx=(0, 8))

        self.model_choice = ttk.Combobox(
            dl_frame,
            values=[m["label"] for m in MODELS.values()],
            state="readonly", width=42,
        )
        self.model_choice.current(0)
        self.model_choice.pack(side="right")

        self._btn(dl_frame, "⬇  הורד", "#6e40c9", self._start_download).pack(
            side="right", padx=(0, 6), ipadx=8, ipady=4)

        # Progress bar (hidden until download starts)
        self.progress_frame = tk.Frame(self, bg="#0d1117")
        self.progress_var  = tk.DoubleVar()
        self.progress_lbl  = tk.StringVar()
        self.progress_bar  = ttk.Progressbar(
            self.progress_frame, variable=self.progress_var,
            maximum=100, length=380,
        )
        self.progress_bar.pack(side="left", padx=(0, 10))
        tk.Label(
            self.progress_frame, textvariable=self.progress_lbl,
            bg="#0d1117", fg="#c9d1d9", width=14,
        ).pack(side="left")

        # Footer
        tk.Label(
            self, text="github.com/g1435r-svg/ASAS",
            bg="#0d1117", fg="#484f58", font=("Segoe UI", 8),
        ).pack(pady=(6, 14))

    def _btn(self, parent, text, color, cmd):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg="white", relief="flat",
            activebackground=color, activeforeground="white",
            cursor="hand2",
        )

    # ------------------------------------------------------------------
    def _check_model_on_start(self) -> None:
        path = find_model()
        if path:
            name = os.path.basename(path)
            self.model_var.set(f"✅  מודל נטען: {name}")
        else:
            self.model_var.set("⚠️  לא נמצא מודל – הורד מודל לפני השיחה")

    # ------------------------------------------------------------------
    def _launch_cli(self) -> None:
        if not self._assert_model():
            return
        model_path = find_model()
        env = {**os.environ, "MODEL_PATH": model_path}
        try:
            subprocess.Popen(
                [python_exe(), CLI_PY],
                env=env,
                cwd=BASE_DIR,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
            )
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("שגיאה", f"לא ניתן להפעיל CLI:\n{exc}")

    def _launch_web(self) -> None:
        if not self._assert_model():
            return
        model_path = find_model()
        env = {**os.environ, "MODEL_PATH": model_path}
        try:
            subprocess.Popen(
                [python_exe(), APP_PY],
                env=env,
                cwd=BASE_DIR,
            )
            # Give the server a moment then open the browser
            self.after(2000, lambda: webbrowser.open("http://localhost:5000"))
            messagebox.showinfo(
                "ממשק ווב",
                "השרת מופעל.\n\nהדפדפן ייפתח אוטומטית לכתובת:\nhttp://localhost:5000\n\n"
                "לסגירה – סגור את חלון ה-launcher.",
            )
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("שגיאה", f"לא ניתן להפעיל שרת ווב:\n{exc}")

    def _assert_model(self) -> bool:
        if find_model():
            return True
        messagebox.showwarning(
            "מודל חסר",
            "לא נמצא מודל.\nהשתמש בלחצן 'הורד' להורדת מודל תחילה.",
        )
        return False

    # ------------------------------------------------------------------
    def _start_download(self) -> None:
        idx   = self.model_choice.current()
        key   = list(MODELS.keys())[idx]
        model = MODELS[key]
        dest  = os.path.join(MODELS_DIR, model["name"])

        if os.path.isfile(dest):
            if not messagebox.askyesno("מודל קיים", f"המודל כבר קיים:\n{dest}\n\nלהוריד מחדש?"):
                return

        # Show progress bar
        self.progress_frame.pack(padx=20, pady=(0, 8))
        self.progress_var.set(0)
        self.progress_lbl.set("מתחיל...")

        threading.Thread(
            target=self._download_thread,
            args=(model["url"], dest),
            daemon=True,
        ).start()

    def _download_thread(self, url: str, dest: str) -> None:
        tmp = dest + ".part"
        try:
            def progress(block_num, block_size, total):
                downloaded = block_num * block_size
                if total > 0:
                    pct = min(downloaded / total * 100, 100)
                    mb  = downloaded / 1_048_576
                    tot = total / 1_048_576
                    self.progress_var.set(pct)
                    self.progress_lbl.set(f"{mb:.0f}/{tot:.0f} MB")
                else:
                    mb = downloaded / 1_048_576
                    self.progress_lbl.set(f"{mb:.0f} MB")

            os.makedirs(MODELS_DIR, exist_ok=True)
            urllib.request.urlretrieve(url, tmp, reporthook=progress)
            os.replace(tmp, dest)

            self.progress_var.set(100)
            self.progress_lbl.set("הושלם ✅")
            self.after(0, self._on_download_done, dest)

        except Exception as exc:  # noqa: BLE001
            if os.path.exists(tmp):
                os.remove(tmp)
            self.after(0, messagebox.showerror, "שגיאת הורדה", str(exc))
            self.after(0, self.progress_frame.pack_forget)

    def _on_download_done(self, dest: str) -> None:
        name = os.path.basename(dest)
        self.model_var.set(f"✅  מודל נטען: {name}")
        messagebox.showinfo("הורדה הושלמה", f"המודל הורד בהצלחה:\n{name}")


# ---------------------------------------------------------------------------
def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
