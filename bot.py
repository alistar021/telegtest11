from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# جایگزین توکن ربات خودت کن
BOT_TOKEN = "8476998300:AAEDNQ01NNmxf4N9ukVhLT8Qtqsnq4gX6Uk"

# تابع پاسخ به دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات شما آماده به کار است ✅")

if __name__ == "__main__":
    # ساخت اپلیکیشن ربات
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # اضافه کردن دستور /start
    app.add_handler(CommandHandler("start", start))

    # اجرای ربات
    print("ربات در حال اجراست...")
    app.run_polling()
