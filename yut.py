import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os

# توکن ربات
TOKEN = "5902797816:AAFYD_WH1k-cvB2T2NvMW3t8Zitv7tU2Bhc"
bot = telebot.TeleBot(TOKEN)

# مسیر دانلود
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# مسیر فایل کوکی
COOKIE_FILE = "/sdcard/Download/youtyube1/Cookiess.txt"

# ذخیره لینک‌ها برای کاربر
user_links = {}

# حذف webhook اگر فعال باشه
bot.delete_webhook()

# start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 سلام!\nلینک‌های یوتیوبت رو (هر لینک در یک خط) بفرست تا برات دانلود کنم.")

# گرفتن لینک‌ها
@bot.message_handler(func=lambda message: True)
def get_links(message):
    links = [line.strip() for line in message.text.splitlines() if line.strip()]
    if not links:
        bot.reply_to(message, "❌ هیچ لینکی پیدا نشد. لطفا دوباره امتحان کن.")
        return

    user_links[message.chat.id] = links
    bot.reply_to(message, f"✅ {len(links)} لینک دریافت شد.\n⏳ در حال دانلود ویدیوها...")
    
    for url in links:
        try:
            file_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
            
            # اگر فایل کوکی وجود دارد، از آن استفاده کن
            ydl_opts = {
                "format": "best",
                "outtmpl": file_path,
                "quiet": True
            }
            if os.path.exists(COOKIE_FILE):
                ydl_opts["cookiefile"] = COOKIE_FILE

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                ext = info.get("ext", "mp4")

                with open(filename, "rb") as f:
                    if ext in ["mp4", "mkv"]:
                        bot.send_video(message.chat.id, f, caption=info.get("title", ""), timeout=60)
                    else:
                        bot.send_audio(message.chat.id, f, caption=info.get("title", ""), timeout=60)
                os.remove(filename)

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ خطا در دانلود {url}:\n{e}")

# شروع polling
bot.polling()
