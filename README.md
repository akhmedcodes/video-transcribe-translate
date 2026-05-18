# Video Transcribe & Translate Bot

A Telegram bot that receives a video, extracts the audio, transcribes speech to text, and translates it into Uzbek.

**Pipeline:** MP4 video → MP3 audio → Text (RU/EN) → Uzbek translation

---

## Features

- Accepts video, round video (video note), and MP4 files sent as documents
- Auto-detects **Russian** or **English** speech
- Translates transcribed text into **Uzbek**
- Optional user whitelist via `ALLOWED_USERS` (private or public mode)

---

## Requirements

| Component | Version |
|-----------|---------|
| OS | Ubuntu 22.04 LTS |
| Python | 3.10 |
| ffmpeg | 4.4+ |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/akhmedcodes/video-transcribe-translate.git
cd video-transcribe-translate
```

### 2. Run the deploy script

```bash
python3 deploy.py
```

`deploy.py` automatically:
- Installs `ffmpeg` via `apt`
- Creates a `venv/` virtual environment
- Installs all packages from `requirements.txt`
- Copies `.env.example` → `.env`

### 3. Set your bot token

Open `.env` and fill in your `BOT_TOKEN`:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

> Get a token from [@BotFather](https://t.me/BotFather) on Telegram.

### 4. Run the bot

```bash
venv/bin/python bot.py
```

---

## Configuration (`.env`)

| Key | Required | Description |
|-----|----------|-------------|
| `BOT_TOKEN` | Yes | Token from BotFather |
| `WHISPER_MODEL` | No | Whisper model size (default: `base`) |
| `ALLOWED_USERS` | No | Comma-separated Telegram user IDs |

### `WHISPER_MODEL` options

| Model | RAM | Speed | Accuracy |
|-------|-----|-------|----------|
| `tiny` | ~1 GB | Fastest | Low |
| `base` | ~1 GB | Fast | Good ✓ |
| `small` | ~2 GB | Medium | Better |
| `medium` | ~5 GB | Slow | Great |
| `large` | ~10 GB | Slowest | Best |

### `ALLOWED_USERS` — access control

```env
# Private mode — only listed users can use the bot
ALLOWED_USERS=123456789,987654321

# Public mode — anyone can use the bot (leave empty)
ALLOWED_USERS=
```

> Find your Telegram user ID by messaging [@userinfobot](https://t.me/userinfobot).

---

## Usage

1. Send an MP4 video to the bot (max 20 MB)
2. The bot processes it and replies with:
   - Detected language
   - Original transcribed text (RU or EN)
   - Uzbek translation

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| [aiogram 2.25.1](https://github.com/aiogram/aiogram) | Telegram Bot API |
| [openai-whisper](https://github.com/openai/whisper) | Speech-to-text |
| [deep-translator](https://github.com/nidhaloff/deep-translator) | Text translation |
| ffmpeg | MP4 → MP3 conversion |

---

## License

MIT
