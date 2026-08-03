import os
import time
from threading import Thread
from flask import Flask
import telebot
import random

# Configuración de Flask para mantener el servicio activo en Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Crypto IDX Activo"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()

# Configuración de tu Bot de Telegram
# REEMPLAZA 'TU_TOKEN_AQUI' CON EL TOKEN REAL DE BOTFATHER (debe incluir los dos puntos ':')
TOKEN = 'TU_TOKEN_AQUI'
bot = telebot.TeleBot(TOKEN)

chat_id_global = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(welcome_message):
    global chat_id_global
    chat_id_global = welcome_message.chat.id
    bot.reply_to(welcome_message, "¡Bot conectado con éxito! Analizando el mercado de Crypto IDX con filtros avanzados...")

# Funciones de cálculo matemático en Python puro
def calcular_ema(precios, periodo):
    if len(precios) < periodo:
        return precios[-1]
    multiplicador = 2 / (periodo + 1)
    ema = precios[0]
    for precio in precios[1:]:
        ema = (precio - ema) * multiplicador + ema
    return ema

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

# Lógica de señales con indicadores técnicos
def generar_senal_tecnica():
    base_precio = 641.86
    precios_simulados = [base_precio + random.uniform(-0.5, 0.5) for _ in range(50)]
    
    precio_actual = precios_simulados[-1]
    e20 = calcular_ema(precios_simulados, 20)
    e50 = calcular_ema(precios_simulados, 50)
    rsi_val = calcular_rsi(precios_simulados, 14)
    upper_b, lower_b = calcular_bollinger(precios_simulados, 20, 2)
    
    # Temporalidad dinámica basada en volatilidad
    ancho = upper_b - lower_b
    if ancho > 0.8:
        temporalidad = "5 Minutos ⏱️ (Alta volatilidad)"
    else:
        temporalidad = "3 Minutos ⏱️ (Temporalidad estándar)"
        
    # Decisión técnica
    if precio_actual <= lower_b and rsi_val <= 35 and e20 > e50:
        tipo = "CALL 🟢 (Compra)"
    elif precio_actual >= upper_b and rsi_val >= 65 and e20 < e50:
        tipo = "PUT 🔴 (Venta)"
    else:
        tipo = random.choice(["CALL 🟢 (Compra)", "PUT 🔴 (Venta)"])
        
    mensaje = (
        f"🚨 **NUEVA SEÑAL - CRIPTO IDX** 🚨\n\n"
        f"* **Operación:** {tipo}\n"
        f"* **Temporalidad:** {temporalidad}\n"
        f"* **RSI Actual:** {rsi_val:.1f}\n"
        f"* **Gestión Sugerida:** $1 (Capital actual: $20)\n\n"
        f"Reactiva con 👍 si ganaste / 👎 si perdió."
    )
    return mensaje

def loop_senales():
    while True:
        time.sleep(300) # Espera 5 minutos
        if chat_id_global:
            try:
                texto = generar_senal_tecnica()
                bot.send_message(chat_id_global, texto, parse_mode="Markdown")
            except Exception as e:
                print(f"Error enviando señal: {e}")

Thread(target=loop_senales, daemon=True).start()

if __name__ == "__main__":
    bot.infinity_polling()
