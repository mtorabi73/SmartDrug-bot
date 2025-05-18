import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client

# اتصال به Hugging Face Space
client = Client("https://mohammadreza73-ag-predictor.hf.space/")

# توکن بات تلگرام (در Railway به صورت ENV تعریف کنید)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# هندلر شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! یک SMILES بفرست تا پیش‌بینی کنم.")

# هندلر پیام متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    smiles = update.message.text.strip()
    try:
        result = client.predict(smiles)
        headers = result['headers']
        data = result['data'][0]
        response = "\n".join([f"{headers[i]}: {data[i]}" for i in range(len(headers))])
        await update.message.reply_text(f"نتیجه پیش‌بینی:\n{response}")
    except Exception as e:
        await update.message.reply_text("خطا در پیش‌بینی. لطفاً دوباره تلاش کنید.")
        print(f"Prediction Error: {e}")

# اجرای بات
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
