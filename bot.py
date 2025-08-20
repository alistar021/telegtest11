from telegram import Bot

# توکن ربات و یوزرنیم کانال
BOT_TOKEN = "8476998300:AAEcUHxNBmBdoYvm3Q3DV9kftBho-ABzJRE"
CHANNEL_USERNAME = "@alialisend123"

# ایجاد نمونه ربات
bot = Bot(token=BOT_TOKEN)

# تست اتصال ربات
try:
    info = bot.get_me()
    print("ربات متصل شد ✅")
    print("نام ربات:", info.first_name)
    print("یوزرنیم ربات:", info.username)
except Exception as e:
    print("اتصال ربات ناموفق ❌")
    print("خطا:", e)

# تست ارسال پیام به کانال
try:
    bot.send_message(chat_id=CHANNEL_USERNAME, text="پیام تست ✅")
    print("ارسال پیام به کانال موفق ✅")
except Exception as e:
    print("ارسال پیام به کانال ناموفق ❌")
    print("خطا:", e)
