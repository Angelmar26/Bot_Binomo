import os
import logging
from flask import Flask
from threading import Thread

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot_Binomo está activo y operando en Render 🚀"

def run_bot():
    """
    Aquí se integrará la lógica principal del bot:
    - Sincronización en bloques de 5 minutos.
    - Indicadores técnicos: EMA (50 y 200), Bandas de Bollinger y RSI (14).
    - Conexión con el bot de Telegram para alertas y registro de resultados.
    """
    logger.info("Iniciando la rutina de análisis técnico y monitoreo de Telegram...")

if __name__ == '__main__':
    # Iniciar el bot en un hilo secundario para que no bloquee el servidor web de Render
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Obtener el puerto asignado por Render (por defecto 10000)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
  
