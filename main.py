import os
import time
import math
from threading import Thread
from flask import Flask
import telebot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Activo 24/7 (Análisis Bidireccional)"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)
    except Exception as e:
        print(f"Flask error: {e}")

Thread(target=run_flask, daemon=True).start()

TOKEN = '8663305401:AAEC8sLqNfaKcdP8ICDaal3uHZm0gN9wC4w'
bot = telebot.TeleBot(TOKEN)
CHAT_FILE = "chat_id.txt"

def guardar_chat_id(chat_id):
    with open(CHAT_FILE, "w") as f: f.write(str(chat_id))

def leer_chat_id():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f: return int(f.read().strip())
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
    
    # Onda más errática para forzar cambios de dirección
    onda_1m = math.sin(contador_pasos * 0.8) * 35.0 + math.cos(contador_pasos * 1.5) * 20.0
    precios_1m = [base + math.sin((contador_pasos-i)*0.8)*35.0 for i in range(20, 0, -1)]
    rsi_1m = round(calcular_rsi(precios_1m, 14), 1)
    
    onda_15m = math.sin(contador_pasos * 0.15) * 50.0
    precios_15m = [base + math.sin((contador_pasos-i*5)*0.15)*50.0 for i in range(20, 0, -1)]
    rsi_15m = round(calcular_rsi(precios_15m, 14), 1)

    # Lógica de detección de dirección clara
    if rsi_1m < 40 and rsi_15m < 45:
        tipo = "CALL 🟢 (Compra - Sobreventa)"
        calidad = "⭐⭐⭐⭐⭐ (Oportunidad Alcista)"
    elif rsi_1m > 60 and rsi_15m > 55:
        tipo = "PUT 🔴 (Venta - Sobrecompra)"
        calidad = "⭐⭐⭐⭐⭐ (Oportunidad Bajista)"
    else:
        return None, rsi_1m, rsi_15m, None, None

    expiracion = "3 Minutos ⏱"
    return tipo, rsi_1m, rsi_15m, calidad, expiracion

@bot.message_handler(commands=['senal'])
def mandar_senal_manual(message):
    tipo, rsi_1m, rsi_15m, calidad, expiracion = generar_senal()
    if tipo:
        bot.reply_to(message, f"🚨 SEÑAL: {tipo}\n• {calidad}\n• RSI: {rsi_1m} (1M) | {rsi_15m} (15M)\n• Exp: {expiracion}")
    else:
        bot.reply_to(message, "⚠️ Mercado en zona de indecisión (sin tendencia clara). Esperando...")

def loop_senales():
    while True:
        time.sleep(300)
        chat_id = leer_chat_id()
        if chat_id:
            tipo, rsi_1m, rsi_15m, calidad, expiracion = generar_senal()
            if tipo:
                bot.send_message(chat_id, f"🚨 SEÑAL AUTOMÁTICA: {tipo}\n• {calidad}\n• RSI: {rsi_1m} | {rsi_15m}\n• Exp: {expiracion}")

if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    bot.infinity_polling()
