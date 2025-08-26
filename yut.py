import telebot
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from io import BytesIO
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
TOKEN = os.getenv("5902797816:AAFYD_WH1k-cvB2T2NvMW3t8Zitv7tU2Bhc")  # یا می‌تونی مستقیماً توکن را اینجا بنویسی
bot = telebot.TeleBot(TOKEN)

# تبدیل عکس به PDF
@bot.message_handler(content_types=['photo'])
def photo_to_pdf(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image = Image.open(BytesIO(downloaded_file))
        pdf_path = "output.pdf"
        image.save(pdf_path, "PDF")

        with open(pdf_path, "rb") as f:
            bot.send_document(message.chat.id, f)
        os.remove(pdf_path)
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا: {str(e)}")

# تبدیل Word به PDF ساده
@bot.message_handler(content_types=['document'])
def word_to_pdf(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        if message.document.file_name.endswith(".docx"):
            doc = Document(BytesIO(downloaded_file))
            text = "\n".join([para.text for para in doc.paragraphs])

            # ساخت PDF ساده با Pillow
            img = Image.new('RGB', (800, 1000), color='white')
            d = ImageDraw.Draw(img)
            d.text((10,10), text, fill=(0,0,0))
            pdf_path = "output.pdf"
            img.save(pdf_path, "PDF")

            with open(pdf_path, "rb") as f:
                bot.send_document(message.chat.id, f)
            os.remove(pdf_path)
        else:
            bot.send_message(message.chat.id, "فایل Word نیست!")
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا: {str(e)}")

# اجرای ربات
bot.polling(none_stop=True)
