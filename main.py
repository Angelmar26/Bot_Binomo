import logging
import os
from flask import Flask
from threading import Thread
import telebot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8891979485:AAGQMNMziGbL6VralAMWNLc_TTvg5hWJBG0"

# 1. Configurar Flask para que corra en segundo plano y mantenga el puerto de Render abierto
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot_Binomo en Render 🚀 Activo y funcionando!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)

flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# 2. Configurar el bot de Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola Angélica! Tu bot de Binomo está activo y conectado correctamente. 🚀")

if __name__ == '__main__':
    logger.info("Iniciando polling del bot de Telegram...")
    bot.infinity_polling(skip_pending=True)
