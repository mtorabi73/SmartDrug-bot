import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

API_URL = "https://huggingface.co/spaces/Mohammadreza73/AG_Predictor/api/predict"
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ساختار SMILES خود را بفرستید:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    smiles = update.message.text.strip()
    try:
        response = requests.post(API_URL, json={"text": smiles})
        if response.status_code == 200:
            result = response.json()
            await update.message.reply_text(f"پیش‌بینی مدل:\n{result}")
        else:
            await update.message.reply_text("خطا در اتصال به مدل.")
    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
