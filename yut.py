import telebot
from PIL import Image

TOKEN = "5902797816:AAFYD_WH1k-cvB2T2NvMW3t8Zitv7tU2Bhc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def photo_to_pdf(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("input.jpg", "wb") as f:
        f.write(downloaded_file)
    
    image = Image.open("input.jpg")
    image.save("output.pdf", "PDF")
    
    with open("output.pdf", "rb") as f:
        bot.send_document(message.chat.id, f)

bot.polling()
