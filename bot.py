import asyncio
import logging
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from deep_translator import GoogleTranslator
import whisper
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny/base/small/medium/large

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
executor_pool = ThreadPoolExecutor(max_workers=2)

log.info("Loading Whisper model '%s'...", WHISPER_MODEL)
model = whisper.load_model(WHISPER_MODEL)
log.info("Whisper model loaded.")


def _convert_to_mp3(mp4_path: str, mp3_path: str) -> None:
    subprocess.run(
        ["ffmpeg", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path, "-y"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _transcribe(mp3_path: str) -> tuple[str, str]:
    result = model.transcribe(mp3_path, language=None, task="transcribe")
    lang = result.get("language", "auto")
    text = result.get("text", "").strip()
    return text, lang


def _translate(text: str, source_lang: str) -> str:
    lang_map = {"ru": "ru", "en": "en"}
    src = lang_map.get(source_lang, "auto")
    return GoogleTranslator(source=src, target="uz").translate(text)


async def run_in_thread(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor_pool, func, *args)


async def process_video(message: types.Message, file_id: str, file_name: str = "video") -> None:
    status = await message.reply("⏳ Video qabul qilindi, qayta ishlanmoqda...")

    with tempfile.TemporaryDirectory() as tmpdir:
        mp4_path = os.path.join(tmpdir, f"{file_name}.mp4")
        mp3_path = os.path.join(tmpdir, f"{file_name}.mp3")

        # 1. Download
        try:
            file = await bot.get_file(file_id)
            await file.download(destination_file=mp4_path)
        except Exception as e:
            log.error("Download error: %s", e)
            await status.edit_text("❌ Faylni yuklab olishda xato yuz berdi.")
            return

        # 2. Convert MP4 → MP3
        await status.edit_text("🔄 MP4 → MP3 ga o'tkazilmoqda...")
        try:
            await run_in_thread(_convert_to_mp3, mp4_path, mp3_path)
        except subprocess.CalledProcessError as e:
            log.error("ffmpeg error: %s", e)
            await status.edit_text("❌ Video konvertatsiyada xato. ffmpeg o'rnatilganligini tekshiring.")
            return

        # 3. Transcribe (RU / EN auto-detect)
        await status.edit_text("🎙 Ovozdan matn tanib olinmoqda...")
        try:
            text, lang = await run_in_thread(_transcribe, mp3_path)
        except Exception as e:
            log.error("Whisper error: %s", e)
            await status.edit_text("❌ Matn tanib olishda xato yuz berdi.")
            return

        if not text:
            await status.edit_text("⚠️ Videoda aniqlanadigan nutq topilmadi.")
            return

        lang_label = {"ru": "Rus", "en": "Ingliz"}.get(lang, lang.upper())
        await status.edit_text(
            f"✅ Aniqlangan til: {lang_label}\n\n"
            f"📝 <b>Asl matn:</b>\n{text}",
            parse_mode="HTML",
        )

        # 4. Translate → UZ
        try:
            translated = await run_in_thread(_translate, text, lang)
            await message.reply(
                f"🇺🇿 <b>O'zbekcha tarjima:</b>\n{translated}",
                parse_mode="HTML",
            )
        except Exception as e:
            log.error("Translation error: %s", e)
            await message.reply("⚠️ Tarjima amalga oshmadi, lekin asl matn yuqorida ko'rsatilgan.")


@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(
        "👋 Salom! Men video → matn → o'zbek tili tarjimachisiman.\n\n"
        "📹 Video yuboring (MP4), men:\n"
        "  1. Ovozni MP3 ga o'zgartiraman\n"
        "  2. Rus yoki ingliz tilida matn tanib olaman\n"
        "  3. O'zbekchaga tarjima qilaman\n\n"
        "📌 Telegram limiti: 20 MB (bot orqali)"
    )


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    await process_video(message, message.video.file_id, "video")


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    await process_video(message, message.video_note.file_id, "videonote")


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    doc = message.document
    mime = doc.mime_type or ""
    if "video" in mime or (doc.file_name or "").lower().endswith(".mp4"):
        await process_video(message, doc.file_id, "document")
    else:
        await message.reply("⚠️ Iltimos, faqat video (MP4) fayl yuboring.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
