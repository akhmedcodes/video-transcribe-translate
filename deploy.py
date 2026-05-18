#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

VENV_DIR = "venv"
REQUIREMENTS = "requirements.txt"


def step(msg: str) -> None:
    print(f"\n\033[1;34m==>\033[0m {msg}")


def ok(msg: str) -> None:
    print(f"  \033[1;32m✔\033[0m {msg}")


def fail(msg: str) -> None:
    print(f"  \033[1;31m✘\033[0m {msg}")
    sys.exit(1)


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kwargs)


def install_ffmpeg() -> None:
    step("ffmpeg o'rnatilmoqda...")
    if shutil.which("ffmpeg"):
        ok("ffmpeg allaqachon o'rnatilgan, o'tkazib yuborildi.")
        return
    try:
        run(["sudo", "apt-get", "update", "-y"])
        run(["sudo", "apt-get", "install", "-y", "ffmpeg"])
        ok("ffmpeg muvaffaqiyatli o'rnatildi.")
    except subprocess.CalledProcessError:
        fail("ffmpeg o'rnatib bo'lmadi. 'sudo apt-get install -y ffmpeg' buyrug'ini qo'lda bajaring.")


def create_venv() -> None:
    step(f"Virtual muhit yaratilmoqda ({VENV_DIR})...")
    if os.path.isdir(VENV_DIR):
        ok(f"'{VENV_DIR}' allaqachon mavjud, o'tkazib yuborildi.")
        return
    try:
        run([sys.executable, "-m", "venv", VENV_DIR])
        ok(f"Virtual muhit '{VENV_DIR}' papkasida yaratildi.")
    except subprocess.CalledProcessError:
        fail("Virtual muhit yaratib bo'lmadi.")


def install_packages() -> None:
    step(f"Paketlar o'rnatilmoqda ({REQUIREMENTS})...")
    if not os.path.isfile(REQUIREMENTS):
        fail(f"'{REQUIREMENTS}' fayli topilmadi.")

    pip = os.path.join(VENV_DIR, "bin", "pip")
    try:
        run([pip, "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
        run([pip, "install", "-r", REQUIREMENTS])
        ok("Barcha paketlar muvaffaqiyatli o'rnatildi.")
    except subprocess.CalledProcessError:
        fail("Paketlarni o'rnatib bo'lmadi.")


def setup_env() -> None:
    step(".env fayli tekshirilmoqda...")
    if os.path.isfile(".env"):
        ok(".env fayli mavjud, o'tkazib yuborildi.")
        return
    if os.path.isfile(".env.example"):
        shutil.copy(".env.example", ".env")
        ok(".env.example → .env nusxa ko'chirildi. Iltimos, BOT_TOKEN ni to'ldiring.")
    else:
        ok(".env.example topilmadi. .env faylini qo'lda yarating.")


def main() -> None:
    print("\033[1;36m" + "=" * 50)
    print("   Video Transcribe & Translate Bot — Deploy")
    print("=" * 50 + "\033[0m")

    if sys.platform != "linux":
        fail("Bu skript faqat Ubuntu/Linux uchun mo'ljallangan.")

    install_ffmpeg()
    create_venv()
    install_packages()
    setup_env()

    print("\n\033[1;32m" + "=" * 50)
    print("  Muvaffaqiyatli o'rnatildi!")
    print("=" * 50 + "\033[0m")
    print("\nKeyingi qadam:")
    print("  1. .env fayliga BOT_TOKEN ni kiriting")
    print(f"  2. Botni ishga tushiring: {VENV_DIR}/bin/python bot.py\n")


if __name__ == "__main__":
    main()
