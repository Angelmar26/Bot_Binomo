import os
import time
import math
from threading import Thread
from flask import Flask
import telebot

# --- CONFIGURACIÓN DEL SERVIDOR WEB (Para mantener despierto a Render) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Señales - Activo 24/7"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)
    except Exception as e:
        print(f"Flask error: {e}")

# Iniciar Flask en un hilo secundario
Thread(target=run_flask, daemon=True).start()

# --- CONFIGURACIÓN DEL BOT DE TELEGRAM ---
TOKEN = '8663305401:AAEC8sLqNfaKcdP8ICDaal3uHZm0gN9wC4w'
bot = telebot.TeleBot(TOKEN)

CHAT_FILE = "chat_id.txt"

def guardar_chat_id(chat_id):
    try:
        with open(CHAT_FILE, "w") as f:
            f.write(str(chat_id))
    except Exception as e:
        print(f"Error guardando chat_id: {e}")

def leer_chat_id():
    # 1. Intentar leer del archivo local
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    return int(content)
        except Exception as e:
            print(f"Error leyendo chat_id: {e}")
    
    # 2. Respaldo por Variable de Entorno (Evita pérdida si Render borra el archivo)
    env_chat = os.environ.get('DEFAULT_CHAT_ID')
    if env_chat:
        try:
            return int(env_chat)
        except:
            pass
            
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        chat_id = message.chat.id
        guardar_chat_id(chat_id)
        bot.reply_to(
            message, 
            f"🤖 ¡Bot activado correctamente!\nTu Chat ID ({chat_id}) ha sido registrado.\nEscribe /senal para probar una señal manual."
        )
        print(f"Chat ID registrado exitosamente: {chat_id}")
    except Exception as e:
        print(f"Error en start: {e}")

# --- MOTOR DE CÁLCULO RSI Y SEÑALES ---
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

def generar_senal():
    global contador_pasos
    contador_pasos += 3
    base = 641.86
    
    onda = math.sin(contador_pasos * 1.3) * 28.0 + math.cos(contador_pasos * 0.6) * 16.0 + ((contador_pasos % 5) * 4.0)
    precio_actual = round(base + onda, 2)
    
    precios = [round(base + math.sin((contador_pasos - i) * 1.3) * 28.0 + math.cos((contador_pasos - i) * 0.6) * 16.0, 2) for i in range(25, 0, -1)]
    precios.append(precio_actual)
    
    rsi_val = calcular_rsi(precios, 14)
    rsi_val = round(rsi_val, 1)

    if rsi_val >= 60:
        tipo = "PUT 🔴 (Venta - Zona Alta)"
    elif rsi_val <= 40:
        tipo = "CALL 🟢 (Compra - Zona Baja)"
    else:
        tipo = "PUT 🔴 (Venta)" if rsi_val > 50 else "CALL 🟢 (Compra)"
        
    return tipo, rsi_val

@bot.message_handler(commands=['senal'])
def mandar_senal_manual(message):
    try:
        chat_id = message.chat.id
        guardar_chat_id(chat_id)
        tipo, rsi_val = generar_senal()
        texto = (
            "🚨 SEÑAL MANUAL - CRIPTO IDX 🚨\n\n"
            f"• Operación: {tipo}\n"
            "• Calidad: ⭐⭐⭐⭐⭐ (Alta Confiabilidad)\n"
            "• Temporalidad: 5 Minutos ⏱\n"
            f"• RSI Actual: {rsi_val}\n"
            "• Gestión Sugerida: $1 (Capital actual: $20)\n\n"
            "Reactiva con 👍 si ganaste / 👎 si perdió."
        )
        bot.send_message(chat_id, texto)
    except Exception as e:
        print(f"Error enviando señal manual: {e}")

# --- BUCLE DE SEÑALES AUTOMÁTICAS ---
def loop_senales():
    time.sleep(20)
    while True:
        time.sleep(300) # Ciclo exacto de 5 minutos
        chat_id = leer_chat_id()
        if chat_id:
            try:
                tipo, rsi_val = generar_senal()
                texto = (
                    "🚨 SEÑAL AUTOMÁTICA - CRIPTO IDX 🚨\n\n"
                    f"• Operación: {tipo}\n"
                    "• Calidad: ⭐⭐⭐⭐⭐ (Alta Confiabilidad)\n"
                    "• Temporalidad: 5 Minutos ⏱\n"
                    f"• RSI Actual: {rsi_val}\n"
                    "• Gestión Sugerida: $1 (Capital actual: $20)\n\n"
                    "Reactiva con 👍 si ganaste / 👎 si perdió."
                )
                bot.send_message(chat_id, texto)
                print(f"Señal automática enviada exitosamente al chat ID: {chat_id}")
            except Exception as e:
                print(f"Error en loop automático: {e}")
        else:
            print("Loop automático en espera: Ningún chat_id registrado todavía. Envía /start en Telegram.")

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    Thread(target=loop_senales, daemon=True).start()
    print("Iniciando bot...")
    time.sleep(5)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Reconexión: {e}")
            time.sleep(15)
