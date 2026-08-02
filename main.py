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
    token_status = f"Configurado correctamente (Largo: {len(TOKEN)})" if TOKEN else "NO DETECTADO ❌"
    return f"Bot_Binomo en Render 🚀<br><br><b>Token:</b> {token_status}"

bot = None
if TOKEN and ":" in TOKEN:
    try:
        bot = telebot.TeleBot(TOKEN)
        bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook eliminado y bot preparado correctamente.")
    except Exception as e:
        logger.error(f"Error al configurar Telegram: {e}")
