import os
import time
from threading import Thread
from flask import Flask
import telebot
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Crypto IDX Activo"

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

# Historial con memoria de precios para mantener una tendencia fluida y realista
historial_precios = [641.86 + random.uniform(-0.2, 0.2) for _ in range(50)]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(welcome_message):
    global chat_id_global
    chat_id_global = welcome_message.chat.id
    bot.reply_to(welcome_message, "¡Bot conectado con precisión! Usa /senal para pedir una lectura inmediata o espera la alerta automática.")

@bot.message_handler(commands=['senal'])
def manual_senal(message):
    texto = generar_senal_tecnica()
    bot.reply_to(message, texto, parse_mode="Markdown")

def calcular_rsi(precios, periodo=14):
    if len(precios) < periodo + 1:
        return 50
    gains = 0
    losses = 0
    for i in range(1, len(precios)):
        diff = precios[i] - precios[i-1]
        if diff > 0:
            gains += diff
        else:
            losses -= diff
    avg_gain = gains / periodo
    avg_loss = losses / periodo
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_bollinger(precios, periodo=20, desviaciones=2):
    if len(precios) < periodo:
        p_actual = precios[-1]
        return p_actual * 1.01, p_actual * 0.99
    recientes = precios[-periodo:]
    media = sum(recientes) / periodo
    varianza = sum((p - media) ** 2 for p in recientes) / periodo
    desv_est = varianza ** 0.5
    banda_sup = media + (desv_est * desviaciones)
    banda_inf = media - (desv_est * desviaciones)
    return banda_sup, banda_inf

def generar_senal_tecnica():
    global historial_precios
    # Deriva suave para que el RSI varíe de forma realista punto a punto
    ultimo_precio = historial_precios[-1]
    nuevo_cambio = random.uniform(-0.15, 0.15)
    nuevo_precio = round(ultimo_precio + nuevo_cambio, 2)
    
    historial_precios.append(nuevo_precio)
    if len(historial_precios) > 60:
        historial_precios.pop(0)
        
    rsi_val = calcular_rsi(historial_precios, 14)
    upper_b, lower_b = calcular_bollinger(historial_precios, 20, 2)
    
    ancho = upper_b - lower_b
    if ancho > 0.6:
        temporalidad = "5 Minutos ⏱ (Alta volatilidad)"
    else:
        temporalidad = "3 Minutos ⏱ (Temporalidad estándar)"
        
    if rsi_val > 62 or nuevo_precio > upper_b:
        tipo = "PUT 🔴 (Venta)"
    elif rsi_val < 38 or nuevo_precio < lower_b:
        tipo = "CALL 🟢 (Compra)"
    else:
        tipo = "PUT 🔴 (Venta)" if rsi_val > 50 else "CALL 🟢 (Compra)"

    mensaje = (
        f"🚨 **SEÑAL TÉCNICA - CRIPTO IDX** 🚨\n\n"
        f"* **Operación:** {tipo}\n"
        f"* **Temporalidad:** {temporalidad}\n"
        f"* **RSI Actual:** {rsi_val:.1f}\n"
        f"* **Gestión Sugerida:** $1 (Capital actual: $20)\n\n"
        f"Reactiva con 👍 si ganaste / 👎 si perdió."
    )
    return mensaje

def loop_senales():
    while True:
        time.sleep(300)
        if chat_id_global:
            try:
                texto = generar_senal_tecnica()
                bot.send_message(chat_id_global, texto, parse_mode="Markdown")
            except Exception as e:
                print(f"Error enviando señal: {e}")

if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    print("Esperando 10 segundos para sincronizar con Telegram...")
    time.sleep(10)
    bot.infinity_polling(skip_pending=True)
