"""
Download a GGUF model for offline use.

Supported models (choose one):
  1. Mistral 7B Instruct Q4_K_M  (~4.1 GB) - מומלץ
  2. Llama-3.2 1B Instruct Q8_0  (~1.3 GB) - קטן ומהיר

Usage:
    python download_model.py          # downloads default (Mistral 7B Q4_K_M)
    python download_model.py --small  # downloads small model (Llama 1B Q8)
"""

import argparse
import os
import sys
import urllib.request

MODELS = {
    "default": {
        "name": "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "url": (
            "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
            "/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        ),
        "size": "~4.1 GB",
    },
    "small": {
        "name": "Llama-3.2-1B-Instruct-Q8_0.gguf",
        "url": (
            "https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
            "/resolve/main/Llama-3.2-1B-Instruct-Q8_0.gguf"
        ),
        "size": "~1.3 GB",
    },
}


def show_progress(block_num: int, block_size: int, total_size: int) -> None:
    downloaded = block_num * block_size
    if total_size > 0:
        pct = min(downloaded / total_size * 100, 100)
        mb = downloaded / 1_048_576
        total_mb = total_size / 1_048_576
        print(f"\r  הורדה: {mb:.1f} / {total_mb:.1f} MB  ({pct:.1f}%)", end="", flush=True)
    else:
        mb = downloaded / 1_048_576
        print(f"\r  הורדה: {mb:.1f} MB", end="", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="הורדת מודל GGUF")
    parser.add_argument("--small", action="store_true", help="הורד מודל קטן (Llama 1B)")
    args = parser.parse_args()

    key = "small" if args.small else "default"
    model = MODELS[key]

    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)
    dest = os.path.join(models_dir, model["name"])

    if os.path.exists(dest):
        print(f"המודל כבר קיים: {dest}")
        return

    print(f"מודל: {model['name']}  ({model['size']})")
    print(f"URL:  {model['url']}")
    print("מוריד... (זה עשוי לקחת מספר דקות)")

    try:
        urllib.request.urlretrieve(model["url"], dest, reporthook=show_progress)
        print(f"\n✅ הורדה הושלמה: {dest}")
    except Exception as exc:  # noqa: BLE001
        print(f"\n❌ שגיאה בהורדה: {exc}")
        if os.path.exists(dest):
            os.remove(dest)
        sys.exit(1)


if __name__ == "__main__":
    main()
