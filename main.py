import logging
import os
from flask import Flask
from threading import Thread
import telebot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8663305401:AAH4Bc428UheAjM1LaMRGYwgbac6SozUjBE"

# 1. Configurar Flask para que corra en segundo plano manteniendo contento a Render
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

# 2. Configurar el bot de Telegram en el hilo principal
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola Angélica! Tu bot nuevo de Binomo está activo y conectado correctamente. 🚀")

if __name__ == '__main__':
    logger.info("Iniciando polling del bot de Telegram...")
    bot.infinity_polling(skip_pending=True)
