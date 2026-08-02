import os
import time
import logging
from flask import Flask
from threading import Thread
import telebot

# Configuración de registros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener token de las variables de entorno
TOKEN = os.environ.get('TELEGRAM_TOKEN', '').strip()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot_Binomo está activo y operando en Render 🚀"

if TOKEN:
    bot = telebot.TeleBot(TOKEN)
    
    # Limpiar cualquier webhook anterior para permitir la lectura de mensajes
    try:
        bot.remove_webhook()
        logger.info("Webhook previo eliminado correctamente.")
    except Exception as e:
        logger.error(f"No se pudo eliminar el webhook: {e}")

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        try:
            bot.reply_to(
                message,
                "📈 **SEÑAL DE BINOMO DETECTADA** 📈\n\n"
                "🟢 **Operación:** ¡Bot Sincronizado y Conectado!\n"
                "🪙 **Activo:** Crypto IDX\n"
                "⏱️ **Temporalidad:** 1 a 5 minutos\n"
                "💡 **Estrategia:** EMA 20 + RSI 14\n"
                "✨ ¡Abundancia y éxito en la operación!",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Error respondiendo /start: {e}")

    def run_telegram_bot():
        logger.info("Iniciando el ciclo del bot de Telegram...")
        while True:
            try:
                bot.infinity_polling(timeout=60, long_polling_timeout=60)
            except Exception as e:
                logger.error(f"Error en polling de Telegram: {e}")
                time.sleep(15)

    # Iniciar el hilo del bot de forma inmediata
    tg_thread = Thread(target=run_telegram_bot)
    tg_thread.daemon = True
    tg_thread.start()
else:
    logger.warning("ATENCIÓN: TELEGRAM_TOKEN no está configurado en las variables de entorno de Render.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
