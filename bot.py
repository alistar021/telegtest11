from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8476998300:AAEcUHxNBmBdoYvm3Q3DV9kftBho-ABzJRE"
CHANNEL_USERNAME = "@alialisend123"

# ====== دستور استارت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام شما به کانال ارسال می‌شود.")

# ====== دریافت پیام و ارسال به کانال ======
async def forward_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    bot = context.bot
    await bot.send_message(chat_id=CHANNEL_USERNAME, text=message_text)
    await update.message.reply_text("پیام شما ارسال شد ✅")

# ====== اجرای ربات ======
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_channel))

app.run_polling()
