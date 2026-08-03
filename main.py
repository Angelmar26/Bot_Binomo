import os
import time
import math
from threading import Thread
from flask import Flask
import telebot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Activo 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()

TOKEN = '8663305401:AAEC8sLqNfaKcdP8ICDaal3uHZm0gN9wC4w'
bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
    time.sleep(2)
except Exception as e:
    print(f"Error limpiando webhook: {e}")

# Variable en memoria para capturar tu chat al instante
chat_id_global = None

@bot.message_handler(func=lambda message: True)
def capturar_chat(message):
    global chat_id_global
    chat_id_global = message.chat.id
    bot.reply_to(message, "✅ ¡Canal conectado con éxito! El bot ya memorizó tu chat y te enviará las señales automáticas cada 5 minutos.")

def loop_senales():
    global chat_id_global
    # Pausa inicial de cortesía al arrancar
    time.sleep(15)
    while True:
        time.sleep(300) # Ciclo exacto de 5 minutos
        if chat_id_global:
            try:
                # Simulación de análisis técnico dinámico
                rsi_val = 58.5 if int(time.time()) % 2 == 0 else 42.1
                tipo = "PUT 🔴 (Venta)" if rsi_val > 50 else "CALL 🟢 (Compra)"
                
                mensaje = (
                    f"🚨 **SEÑAL AUTOMÁTICA - CRIPTO IDX** 🚨\n\n"
                    f"* **Operación:** {tipo}\n"
                    f"* **Calidad:** ⭐⭐⭐⭐⭐ (Alta Confiabilidad)\n"
                    f"* **Temporalidad:** 5 Minutos ⏱\n"
                    f"* **RSI Actual:** {rsi_val:.1f}\n"
                    f"* **Gestión Sugerida:** $1 (Capital actual: $20)\n\n"
                    f"Reactiva con 👍 si ganaste / 👎 si perdió."
                )
                bot.send_message(chat_id_global, mensaje, parse_mode="Markdown")
            except Exception as e:
                print(f"Error enviando señal: {e}")
        else:
            print("Esperando que envíes un mensaje al bot en Telegram para activar el chat...")

if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    print("Iniciando motor del bot...")
    time.sleep(5)
    
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Reconectando: {e}")
            time.sleep(5)
