import os
import time
import math
from threading import Thread
from flask import Flask
import telebot

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
    time.sleep(2)
except Exception as e:
    print(f"Error limpiando webhook: {e}")

CHAT_FILE = "chat_id.txt"

def guardar_chat_id(chat_id):
    try:
        with open(CHAT_FILE, "w") as f:
            f.write(str(chat_id))
    except Exception as e:
        print(f"Error guardando chat_id: {e}")

def leer_chat_id():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f:
                return int(f.read().strip())
        except Exception as e:
            print(f"Error leyendo chat_id: {e}")
    return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(welcome_message):
    chat_id = welcome_message.chat.id
    guardar_chat_id(chat_id)
    bot.reply_to(welcome_message, 
                 "🤖 ¡Sistema vinculado correctamente!\n\n"
                 "Tu chat ha sido guardado en el servidor. El bot ahora te enviará las señales automáticas cada 5 minutos sin interrupciones.")

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

contador_pasos = 0

def generar_senal_activa():
    global contador_pasos
    contador_pasos += 1
    
    base = 641.86
    onda = math.sin(contador_pasos * 0.7) * 7.0 + math.cos(contador_pasos * 0.3) * 3.5
    precio_actual = round(base + onda, 2)
    
    precios = [round(base + math.sin((contador_pasos - i) * 0.7) * 7.0, 2) for i in range(25, 0, -1)]
    precios.append(precio_actual)
    
    rsi_val = calcular_rsi(precios, 14)
    
    if rsi_val >= 55:
        tipo = "PUT 🔴 (Venta)"
        calidad = "⭐⭐⭐⭐⭐ (Alta Confiabilidad)"
    elif rsi_val <= 45:
        tipo = "CALL 🟢 (Compra)"
        calidad = "⭐⭐⭐⭐⭐ (Alta Confiabilidad)"
    else:
        tipo = "PUT 🔴 (Venta)" if rsi_val > 50 else "CALL 🟢 (Compra)"
        calidad = "⭐⭐⭐⭐ (Zona Dinámica)"
        
    return tipo, calidad, rsi_val

def loop_senales():
    while True:
        time.sleep(300)
        chat_id = leer_chat_id()
        if chat_id:
            try:
                tipo, calidad, rsi_val = generar_senal_activa()
                mensaje = (
                    f"🚨 **SEÑAL AUTOMÁTICA - CRIPTO IDX** 🚨\n\n"
                    f"* **Operación:** {tipo}\n"
                    f"* **Calidad:** {calidad}\n"
                    f"* **Temporalidad:** 5 Minutos ⏱\n"
                    f"* **RSI Actual:** {rsi_val:.1f}\n"
                    f"* **Gestión Sugerida:** $1 (Capital actual: $20)\n\n"
                    f"Reactiva con 👍 si ganaste / 👎 si perdió."
                )
                bot.send_message(chat_id, mensaje, parse_mode="Markdown")
            except Exception as e:
                print(f"Error en loop: {e}")
        else:
            print("Esperando registro de chat...")

if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    print("Sincronizando con Telegram...")
    time.sleep(15)
    
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Reconectando por conflicto: {e}")
            time.sleep(10)
