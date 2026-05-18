# Video Transcribe & Translate Bot

Telegram bot: video yuborasiz — matn olinadi va o'zbekchaga tarjima qilinadi.

**Pipeline:** MP4 video → MP3 audio → Matn (RU/EN) → O'zbekcha tarjima

---

## Imkoniyatlar

- Video, doiraviy video va hujjat sifatida yuborilgan MP4 fayllarni qabul qiladi
- Ovozni avtomatik ravishda **Rus** yoki **Ingliz** tilida taniydi
- Matnni **O'zbek** tiliga tarjima qiladi
- `ALLOWED_USERS` orqali foydalanuvchilarni cheklash imkoniyati (shaxsiy/ommaviy rejim)

---

## Talab qilinadigan muhit

| Komponent | Versiya |
|-----------|---------|
| OS | Ubuntu 22.04 LTS |
| Python | 3.10 |
| ffmpeg | 4.4+ |

---

## O'rnatish

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/akhmedcodes/video-transcribe-translate.git
cd video-transcribe-translate
```

### 2. Avtomatik o'rnatish

```bash
python3 deploy.py
```

`deploy.py` quyidagilarni bajaradi:
- `ffmpeg` ni `apt` orqali o'rnatadi
- `venv/` virtual muhitini yaratadi
- `requirements.txt` dagi barcha paketlarni o'rnatadi
- `.env.example` dan `.env` faylini yaratadi

### 3. Bot tokenini sozlash

`.env` faylini oching va `BOT_TOKEN` ni to'ldiring:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

> Token olish uchun Telegram'da [@BotFather](https://t.me/BotFather) ga murojaat qiling.

### 4. Botni ishga tushirish

```bash
venv/bin/python bot.py
```

---

## Konfiguratsiya (`.env`)

| Kalit | Majburiy | Tavsif |
|-------|----------|--------|
| `BOT_TOKEN` | Ha | BotFather dan olingan token |
| `WHISPER_MODEL` | Yo'q | Whisper model o'lchami (default: `base`) |
| `ALLOWED_USERS` | Yo'q | Ruxsat berilgan foydalanuvchi IDlari (vergul bilan) |

### `WHISPER_MODEL` tanlash

| Model | RAM | Tezlik | Aniqlik |
|-------|-----|--------|---------|
| `tiny` | ~1 GB | Eng tez | Past |
| `base` | ~1 GB | Tez | Yaxshi ✓ |
| `small` | ~2 GB | O'rta | Yaxshiroq |
| `medium` | ~5 GB | Sekin | A'lo |
| `large` | ~10 GB | Eng sekin | Eng yuqori |

### `ALLOWED_USERS` — kirish huquqini cheklash

```env
# Faqat ko'rsatilgan foydalanuvchilarga ruxsat (shaxsiy rejim)
ALLOWED_USERS=123456789,987654321

# Bo'sh qoldirilsa — bot ommaviy (hamma foydalana oladi)
ALLOWED_USERS=
```

> O'z Telegram ID raqamingizni bilish uchun [@userinfobot](https://t.me/userinfobot) ga yozing.

---

## Foydalanish

1. Botga MP4 video yuboring (max 20 MB)
2. Bot videoni qayta ishlaydi va quyidagilarni yuboradi:
   - Aniqlangan til
   - Asl matn (RU yoki EN)
   - O'zbekcha tarjima

---

## Texnologiyalar

| Kutubxona | Maqsad |
|-----------|--------|
| [aiogram 2.25.1](https://github.com/aiogram/aiogram) | Telegram Bot API |
| [openai-whisper](https://github.com/openai/whisper) | Nutqni matnga aylantirish |
| [deep-translator](https://github.com/nidhaloff/deep-translator) | Matnni tarjima qilish |
| ffmpeg | MP4 → MP3 konvertatsiya |

---

## Litsenziya

MIT
