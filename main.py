import os
from flask import Flask
from threading import Thread
import telebot

TOKEN = 8663305401:AAH4Bc428UheAjMlLaMRGYwgbac6SozUjBE

app = Flask(__name__)

@app.route('/')
def home():
    return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), use_reloader=False)

Thread(target=run_flask, daemon=True).start()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send(message):
    bot.reply_to(message, "¡Listo y funcionando! 🚀")

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
