from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات
BOT_TOKEN = "8476998300:AAGmZpHiHEpe69PERCBnrPnhXdpV5oaEjaY"

# آیدی کانال مقصد (کانال باید Public باشه و ربات داخلش ادمین باشه)
CHANNEL_USERNAME = "@alialisend123"

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n"
        f"هر پیامی با دستور /send بفرستی → به کانال {CHANNEL_USERNAME} میره ✅"
    )

# دستور send
async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await context.bot.send_message(
            chat_id=CHANNEL_USERNAME, 
            text=f"📩 پیام از {update.message.from_user.first_name}:\n\n{update.message.text}"
        )
        await update.message.reply_text("✅ پیام به کانال فرستاده شد!")

# اجرای ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", forward))

    app.run_polling()

if __name__ == "__main__":
    main()
