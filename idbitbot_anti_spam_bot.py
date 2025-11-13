from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTy>
import re

# Ganti dengan token bot kamu
TOKEN = "7764977032:AAGUQZsU94mch3A9o9222QfRp0se5S4eHR0"

# Daftar domain yang diizinkan (misalnya link resmi kamu)
ALLOWED_DOMAINS = ["idbit.org", "web3.idbit.org", "docs.idbit.org", "idbit.io",>

# Kata-kata spam atau terlarang
BLOCKED_WORDS = ["airdrop", "bonus gratis", "porn", "casino", "xxx", "pump"]

async def delete_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text.lower()

    # Deteksi link
    links = re.findall(r"(https?://[^\s]+)", text)

    # Jika ada link yang bukan domain diizinkan → hapus
    if links:
        if not any(allowed in link for allowed in ALLOWED_DOMAINS for link in links):
            await message.delete()
            print(f"🚫 Hapus link tidak diizinkan dari @{message.from_user.username}")
            return

    # Jika ada kata spam → hapus
    if any(word in text for word in BLOCKED_WORDS):
        await message.delete()
        print(f"🚫 Hapus spam dari @{message.from_user.username}")
        return

    # Cegah mention massal
    if "@everyone" in text or "@all" in text:
        await message.delete()
        print(f"🚫 Hapus mention massal dari @{message.from_user.username}")
        return

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_spam))
    print("🤖 Bot anti-spam berjalan...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

