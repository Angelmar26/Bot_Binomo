import os
import time
from threading import Thread
from flask import Flask
import telebot
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Crypto IDX Activo (Modo Estricto)"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()

TOKEN = '8663305401:AAEC8sLqNfaKcdP8ICDaal3uHZm0gN9wC4w'
bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
    time.sleep(1)
except Exception as e:
    print(f"Error limpiando webhook: {e}")

chat_id_global = None
historial_precios = [641.86 + random.uniform(-0.2, 0.2) for _ in range(50)]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(welcome_message):
    global chat_id_global
    chat_id_global = welcome_message.chat.id
    bot.reply_to(welcome_message, 
                 "¡Bot en Modo Estricto Activo!\n\n"
                 "Usa `/senal [valor_rsi]` con el número exacto de tu pantalla para evaluar una entrada de alta probabilidad.")

@bot.message_handler(commands=['senal'])
def manual_senal(message):
    try:
        partes = message.text.split()
        if len(partes) > 1:
            rsi_val = float(partes[1])
        else:
            bot.reply_to(message, "⚠️ Debes incluir el valor del RSI. Ejemplo: `/senal 72`", parse_mode="Markdown")
            return
            
        # FILTROS ESTRICTOS DE ALTA PROBABILIDAD
        if rsi_val >= 68:
            tipo = "PUT 🔴 (Venta - Sobrecompra Fuerte)"
            temporalidad = "5 Minutos ⏱ (Alta Confluencia)"
            calidad = "⭐⭐⭐⭐⭐ (Alta Confiabilidad)"
        elif rsi_val <= 32:
            tipo = "CALL 🟢 (Compra - Sobreventa Fuerte)"
            temporalidad = "5 Minutos ⏱ (Alta Confluencia)"
            calidad = "⭐⭐⭐⭐⭐ (Alta Confiabilidad)"
        else:
            bot.reply_to(message, f"⚠️ RSI Actual: {rsi_val:.1f}. El mercado está en zona neutra (entre 33 y 67). **No hay operación segura en este momento.** Espera un punto extremo.", parse_mode="Markdown")
            return

        mensaje = (
            f"🚨 **SEÑAL DE ALTA PRECISIÓN - CRIPTO IDX** 🚨\n\n"
            f"* **Operación:** {tipo}\n"
            f"* **Calidad:** {calidad}\n"
            f"* **Temporalidad:** {temporalidad}\n"
            f"* **RSI Analizado:** {rsi_val:.1f}\n"
            f"* **Gestión Sugerida:** $1 (Capital actual: $20)\n\n"
            f"Reactiva con 👍 si ganaste / 👎 si perdió."
        )
        bot.reply_to(message, mensaje, parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "⚠️ Formato inválido. Usa un número, por ejemplo: `/senal 71.5`", parse_mode="Markdown")

def loop_senales():
    while True:
        time.sleep(300)
        if chat_id_global:
            try:
                bot.send_message(chat_id_global, "⏰ Han pasado 5 minutos. Revisa si el RSI en tu gráfica tocó extremos (>68 o <32) y usa /senal [valor] para validar.", parse_mode="Markdown")
            except Exception as e:
                print(f"Error en aviso automático: {e}")

if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    print("Esperando 10 segundos para sincronizar con Telegram...")
    time.sleep(10)
    bot.infinity_polling(skip_pending=True)
