import logging
import os
from flask import Flask
from threading import Thread
import telebot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

raw_token = os.environ.get('TELEGRAM_TOKEN', '')
TOKEN = raw_token.replace('\n', '').replace('\r', '').replace(' ', '').strip()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot_Binomo en Render 🚀 Activo y funcionando!"

bot = telebot.TeleBot(TOKEN) if TOKEN and ":" in TOKEN else None

if bot:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "¡Hola Angélica! Tu bot de Binomo está activo y conectado correctamente. 🚀")

    def run_bot():
        logger.info("Iniciando polling del bot de Telegram...")
        bot.infinity_polling(skip_pending=True)

    # Iniciar el bot en un hilo separado para que no bloquee a Flask
    t = Thread(target=run_bot)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
