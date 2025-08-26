import telebot
from PIL import Image
from docx import Document
from io import BytesIO
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# تبدیل عکس به PDF
@bot.message_handler(content_types=['photo'])
def photo_to_pdf(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # ذخیره عکس و تبدیل به PDF
    image = Image.open(BytesIO(downloaded_file))
    pdf_path = "output.pdf"
    image.save(pdf_path, "PDF")

    # ارسال فایل PDF به کاربر
    with open(pdf_path, "rb") as f:
        bot.send_document(message.chat.id, f)
    os.remove(pdf_path)

# تبدیل Word به PDF (خواندن ساده متن و ایجاد PDF)
@bot.message_handler(content_types=['document'])
def word_to_pdf(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    if message.document.file_name.endswith(".docx"):
        doc = Document(BytesIO(downloaded_file))
        text = "\n".join([para.text for para in doc.paragraphs])

        # ساخت PDF ساده با Pillow
        from PIL import Image, ImageDraw, ImageFont
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

# اجرای ربات
bot.polling(none_stop=True)
