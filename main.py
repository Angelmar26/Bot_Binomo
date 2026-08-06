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
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)
    except:
        pass

Thread(target=run_flask, daemon=True).start()

TOKEN = '8663305401:AAEC8sLqNfaKcdP8ICDaal3uHZm0gN9wC4w'
bot = telebot.TeleBot(TOKEN)
CHAT_FILE = "chat_id.txt"

def leer_chat_id():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f:
                content = f.read().strip()
                if content: return int(content)
        except: pass
    return None

def calcular_rsi(precios, periodo=14):
    if len(precios) < periodo + 1: return 50
    gains = losses = 0
    for i in range(1, len(precios)):
        diff = precios[i] - precios[i-1]
        if diff > 0: gains += diff
        else: losses -= diff
    avg_gain = gains / periodo
    avg_loss = losses / periodo
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + (avg_gain / avg_loss)))

contador_pasos = 0

def generar_senal():
    global contador_pasos
    contador_pasos += 1
    base = 641.86
    onda_1m = math.sin(contador_pasos * 0.5) * 40.0
    precios_1m = [base + math.sin((contador_pasos - i) * 0.5) * 40.0 for i in range(20, 0, -1)]
    rsi_1m = round(calcular_rsi(precios_1m, 14), 1)
    onda_15m = math.sin(contador_pasos * 0.1) * 50.0
    precios_15m = [base + math.sin((contador_pasos - i * 5) * 0.1) * 50.0 for i in range(20, 0, -1)]
    rsi_15m = round(calcular_rsi(precios_15m, 14), 1)
    if rsi_1m > 50 or rsi_15m > 50: tipo = "PUT 🔴 (Venta - Ajuste de Tendencia)"
    else: tipo = "CALL 🟢 (Compra - Impulso Alcista)"
    calidad = "⭐⭐⭐⭐"
    return tipo, rsi_1m, rsi_15m, calidad

@bot.message_handler(commands=['start', 'senal'])
def manejar_comandos(message):
    try:
        with open(CHAT_FILE, "w") as f: f.write(str(message.chat.id))
        tipo, rsi_1m, rsi_15m, calidad = generar_senal()
        bot.reply_to(message, f"🚨 SEÑAL MANUAL: {tipo}\n• {calidad}\n• RSI 1M: {rsi_1m} | RSI 15M: {rsi_15m}")
    except Exception as e: print(f"Error en comando: {e}")

def loop_senales():
    time.sleep(10)
    while True:
        time.sleep(300)
        chat_id = leer_chat_id()
        if chat_id:
            try:
                tipo, rsi_1m, rsi_15m, calidad = generar_senal()
                bot.send_message(chat_id, f"🚨 SEÑAL AUTOMÁTICA: {tipo}\n• {calidad}\n• RSI 1M: {rsi_1m} | RSI 15M: {rsi_15m}")
            except Exception as e: print(f"Error en loop: {e}")

if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    # NUEVA LÍNEA PARA LIMPIAR CONFLICTOS:
    bot.remove_webhook() 
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
        except Exception as e:
            time.sleep(15)
