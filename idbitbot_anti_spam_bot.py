from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re

# ==============================
# CONFIG BOT
# ==============================

TOKEN = "7764977032:AAGUQZsU94mch3A9o9222QfRp0se5S4eHR0"

# Domain yang diizinkan
ALLOWED_DOMAINS = [
    "idbit.org",
    "web3.idbit.org",
    "docs.idbit.org",
    "idbit.io",
]

# Kata spam / terlarang
BLOCKED_WORDS = [
    "airdrop",
    "bonus gratis",
    "porn",
    "casino",
    "xxx",
    "pump",
]

# ==============================
# HANDLER
# ==============================

async def delete_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()

    # Deteksi link
    links = re.findall(r"(https?://[^\s]+)", text)

    # Hapus jika ada link yang tidak diizinkan
    if links:
        if not any(allowed in link for allowed in ALLOWED_DOMAINS for link in links):
            await message.delete()
            print(f"🚫 Hapus link tidak diizinkan dari @{message.from_user.username}")
            return

    # Hapus jika ada kata spam
    if any(word in text for word in BLOCKED_WORDS):
        await message.delete()
        print(f"🚫 Hapus spam dari @{message.from_user.username}")
        return

    # Hapus mention massal
    if "@everyone" in text or "@all" in text:
        await message.delete()
        print(f"🚫 Hapus mention massal dari @{message.from_user.username}")
        return

# ==============================
# MAIN BOT
# ==============================

if __name__ == "__main__":
    # Buat aplikasi bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Tambahkan handler untuk semua teks (kecuali command)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_spam))

    print("🤖 Bot anti-spam berjalan...")

    # Jalankan bot
    app.run_polling()

