from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client

client = Client("Mohammadreza73/AG_Predictor")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ساختار SMILES خود را بفرستید:")

async def handle_smiles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        result = client.predict(user_input)
        await update.message.reply_text(f"نتیجه پیش‌بینی:\n{result}")
    except Exception as e:
        await update.message.reply_text(f"خطا در پردازش: {e}")

if __name__ == '__main__':
    from os import getenv
    import asyncio

    # اگر Railway استفاده می‌کنی، توکن رو به‌صورت متغیر محیطی بذار
    BOT_TOKEN = getenv("BOT_TOKEN") or "توکن واقعی ربات را اینجا قرار بده"

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_smiles))

    app.run_polling()
