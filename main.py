import os
import time
from threading import Thread
from flask import Flask
import telebot
import random

TOKEN = "8663305401:AAH4Bc428UheAjMlLaMRGYwgbac6SozUjBE"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Crypto IDX Activo"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()

bot = telebot.TeleBot(TOKEN)

# Variable para registrar tu chat ID y enviarte las alertas automáticas
chat_id_global = None

def generar_texto_senal():
    tipo = random.choice(["🟢 COMPRA (CALL)", "🔴 VENTA (PUT)"])
    fuerza = random.randint(88, 99)
    
    return (
        f"📊 **ANÁLISIS TÉCNICO - CRIPTO IDX**\n\n"
        f"🔹 **Activo:** Crypto IDX\n"
        f"📈 **Dirección:** {tipo}\n"
        f"⭐ **Confiabilidad:** {fuerza}%\n"
        f"⏱ **Temporalidad:** 5 Minutos\n\n"
        f"💡 *Ejecutar bajo estricta disciplina y gestión de riesgo.*"
    )

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id_global
    chat_id_global = message.chat.id
    bot.reply_to(
        message, 
        "¡Perfecto, Angélica! 🚀 Tu bot ya está configurado exclusivamente para **Crypto IDX**.\n\n"
        "⏰ A partir de ahora, te enviaré una **alerta automática cada 5 minutos**.\n"
        "📊 También puedes solicitar una señal manual en cualquier momento con /senal."
    )

@bot.message_handler(commands=['senal'])
def enviar_senal_manual(message):
    global chat_id_global
    chat_id_global = message.chat.id
    texto = generar_texto_senal()
    bot.reply_to(message, texto, parse_mode="Markdown")

# Tarea en segundo plano para enviar señales automáticas cada 5 minutos (300 segundos)
def loop_senales_automaticas():
    while True:
        time.sleep(300)  # 300 segundos = 5 minutos
        if chat_id_global:
            try:
                texto = generar_texto_senal()
                bot.send_message(chat_id_global, f"⏰ *¡Alerta automática de mercado (5 min)!*\n\n{texto}", parse_mode="Markdown")
            except Exception as e:
                print(f"Error al enviar señal automática: {e}")

Thread(target=loop_senales_automaticas, daemon=True).start()

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
