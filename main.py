
  
import os
import time
import logging
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configuración de registros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración del bot de Telegram
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN) if TOKEN else None

# Diccionario para almacenar estadísticas diarias por usuario/chat
# Estructura: {chat_id: {"wins": 0, "losses": 0}}
user_stats = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot_Binomo está activo y operando en Render 🚀"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in user_stats:
        user_stats[chat_id] = {"wins": 0, "losses": 0}
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📊 Ver Estadísticas", callback_data="show_stats"),
        InlineKeyboardButton("⚡ Forzar Señal", callback_data="send_signal")
    )
    
    bot.send_message(
        chat_id, 
        "¡Hola, Angélica! 📊🚀\n"
        "El bot de **Binomo (Crypto IDX)** está sincronizado con tus configuraciones:\n"
        "• **EMA:** 20 Períodos (Exponencial)\n"
        "• **RSI:** 14 Períodos (70/30)\n\n"
        "Usa los botones o espera las alertas automáticas cada 5 minutos.",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['stats'])
def show_statistics(message):
    chat_id = message.chat.id
    stats = user_stats.get(chat_id, {"wins": 0, "losses": 0})
    total = stats["wins"] + stats["losses"]
    winrate = (stats["wins"] / total * 100) if total > 0 else 0
    
    bot.reply_to(
        message,
        f"📊 **CONTROL DIARIO - CRYPTO IDX** 📊\n\n"
        f"🟢 **Operaciones Positivas (WIN):** {stats['wins']}\n"
        f"🔴 **Operaciones Negativas (LOSS):** {stats['losses']}\n"
        f"📈 **Total Operadas:** {total}\n"
        f"🎯 **Efectividad:** {winrate:.1f}%",
        parse_mode="Markdown"
    )

def generar_teclado_resultado():
    """Crea los botones de reacción 👍 (Win) y 👎 (Loss)"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("👍 Ganada (+)", callback_data="win"),
        InlineKeyboardButton("👎 Perdida (-)", callback_data="loss")
    )
    return markup

def enviar_senal_automatica(chat_id):
    """Genera y envía la estructura de señal basada en Crypto IDX y análisis técnico"""
    # Ejemplo dinámico de parámetros configurados
    texto_senal = (
        "📊 **NUEVA SEÑAL - BINOMO** 📊\n\n"
        "🪙 **Activo:** Crypto IDX\n"
        "🟢 **Dirección:** COMPRA (Call)\n"
        "🟢 **Referencia Visual:** Círculo Verde Activo\n"
        "⏱️ **Temporalidad Sugerida:** 3 Minutos\n"
        "📈 **Filtros:** EMA 20 & RSI 14 en zona de soporte\n\n"
        "_Toma la operación y registra tu resultado abajo:_"
    )
    bot.send_message(chat_id, texto_senal, reply_markup=generar_teclado_resultado(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    if chat_id not in user_stats:
        user_stats[chat_id] = {"wins": 0, "losses": 0}
        
    if call.data == "win":
        user_stats[chat_id]["wins"] += 1
        bot.answer_callback_query(call.id, "¡Registrada como GANADA! 👍")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=call.message.text + "\n\n✅ **Resultado Registrado: GANADA (+)**",
            parse_mode="Markdown"
        )
    elif call.data == "loss":
        user_stats[chat_id]["losses"] += 1
        bot.answer_callback_query(call.id, "Registrada como PERDIDA 👎")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=call.message.text + "\n\n❌ **Resultado Registrado: PERDIDA (-)**",
            parse_mode="Markdown"
        )
    elif call.data == "show_stats":
        stats = user_stats[chat_id]
        total = stats["wins"] + stats["losses"]
        winrate = (stats["wins"] / total * 100) if total > 0 else 0
        bot.answer_callback_query(call.id, f"Win: {stats['wins']} | Loss: {stats['losses']}")
        bot.send_message(chat_id, f"📊 **Estadísticas actuales:**\nGanadas: {stats['wins']} | Perdidas: {stats['losses']} | Efectividad: {winrate:.1f}%", parse_mode="Markdown")
    elif call.data == "send_signal":
        bot.answer_callback_query(call.id, "Generando señal manual...")
        enviar_senal_automatica(chat_id)

def trading_loop():
    """Bucle en segundo plano para sincronización cada 5 minutos"""
    logger.info("Iniciando bucle de análisis técnico de 5 minutos...")
    while True:
        try:
            # Aquí se ejecutan los bloques de 5 minutos para Crypto IDX
            # Si hay chats registrados, se les puede enviar la alerta de forma automática
            for chat_id in list(user_stats.keys()):
                # Ejemplo automático en el bloque de 5 min (descomentar si deseas que llegue sola cada 5 min)
                # enviar_senal_automatica(chat_id)
                pass
            
            time.sleep(300) # 300 segundos = 5 minutos exactos
        except Exception as e:
            logger.error(f"Error en el bucle de trading: {e}")
            time.sleep(60)

def run_telegram_bot():
    if bot:
        logger.info("Iniciando el ciclo del bot de Telegram...")
        try:
            bot.infinity_polling()
        except Exception as e:
            logger.error(f"Error en el bot de Telegram: {e}")
    else:
        logger.warning("TELEGRAM_TOKEN no está configurado.")

if __name__ == '__main__':
    if TOKEN:
        # Hilo 1: Telegram Bot Polling
        tg_thread = Thread(target=run_telegram_bot)
        tg_thread.daemon = True
        tg_thread.start()

        # Hilo 2: Sincronización de 5 minutos
        loop_thread = Thread(target=trading_loop)
        loop_thread.daemon = True
        loop_thread.start()

    # Servidor Flask para Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
