from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن جدید
BOT_TOKEN = "8476998300:AAEDNQ01NNmxf4N9ukVhLT8Qtqsnq4gX6Uk"
CHANNEL_USERNAME = "@alialisend123"   # اینو تغییر بده به یوزرنیم کانالت

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"سلام {update.effective_user.first_name} 👋\n"
        f"برای دسترسی به محتوای ربات لطفاً وارد کانال ما بشید:\n{CHANNEL_USERNAME}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # اضافه کردن دستور start
    app.add_handler(CommandHandler("start", start))

    print("ربات روشن شد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
