import os
import time
import logging
from flask import Flask
from threading import Thread
import telebot

# Configuración de registros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener token y limpiar cualquier espacio o salto de línea oculto del teléfono
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
        bot.remove_webhook()
        logger.info("Bot de Telegram inicializado correctamente.")
    except Exception as e:
        logger.error(f"Error al configurar Telegram: {e}")
else:
    logger.warning("ATENCIÓN: TELEGRAM_TOKEN está vacío o formato incorrecto.")

if bot:
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
        while True:
            try:
                bot.infinity_polling(timeout=60, long_polling_timeout=60)
            except Exception as e:
                logger.error(f"Error en polling de Telegram: {e}")
                time.sleep(15)

    tg_thread = Thread(target=run_telegram_bot)
    tg_thread.daemon = True
    tg_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
