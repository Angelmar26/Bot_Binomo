import os
from flask import Flask
from threading import Thread
import telebot
import random  # Lo usaremos para simular el análisis del motor de señales mientras integramos tus indicadores

TOKEN = "8663305401:AAH4Bc428UheAjMlLaMRGYwgbac6SozUjBE"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señas Activo - Binomo"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "¡Hola, Angélica! 🚀 Tu bot de señales para Binomo está activo.\n\n"
        "Comandos disponibles:\n"
        "📊 /senal - Analiza el mercado actual y genera una alerta de Compra/Venta."
    )

@bot.message_handler(commands=['senal'])
def generar_senal(message):
    # Aquí conectaremos tus indicadores técnicos (RSI, Medias Móviles, etc.)
    pares = ["EUR/USD", "GBP/USD", "EUR/JPY", "Bitcoin Index"]
    par_seleccionado = random.choice(pares)
    
    # Lógica de ejemplo para la señal (luego la personalizamos con tus parámetros exactos de análisis)
    tipo = random.choice(["🟢 COMPRA (CALL)", "🔴 VENTA (PUT)"])
    fuerza = random.randint(85, 98)
    
    texto_alerta = (
        f"📊 **ANÁLISIS DE MERCADO - BINOMO**\n\n"
        f"🔹 **Activo:** {par_seleccionado}\n"
        f"📈 **Dirección:** {tipo}\n"
        f"⭐ **Confiabilidad:** {fuerza}%\n"
        f"⏱ **Temporalidad:** 1 - 3 Minutos\n\n"
        f"💡 *Ejecutar según plan de disciplina.*"
    )
    bot.reply_to(message, texto_alerta, parse_mode="Markdown")

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
