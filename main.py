import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
import os

# مقداردهی به Token ربات از محیط Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

# اتصال به Hugging Face Space
client = Client("Mohammadreza73/AG_Predictor")

# تنظیمات مربوط به لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ساختار SMILES خود را بفرستید:")

# هندل پیام‌های متنی شامل SMILES
async def handle_smiles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    smiles = update.message.text
    try:
        prediction = client.predict(smiles)  # فراخوانی مدل
        await update.message.reply_text(f"نتیجه پیش‌بینی: {prediction}")
    except Exception as e:
        logging.error(f"خطا در پیش‌بینی مدل: {e}")
        await update.message.reply_text("خطا در پیش‌بینی مدل.")

# راه‌اندازی ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_smiles))

    app.run_polling()
