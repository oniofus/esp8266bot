from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import paho.mqtt.client as mqtt
import logging


TOKEN = '8119566961:AAGpJE-6pT1vyqwL7sEBqzNJZBDa7MCDxwk'
CHAT_ID = '5033674020'


MQTT_BROKER = "broker.hivemq.com"
TOPIC_CMD = "home/esp1/cmd"
TOPIC_STATUS = "home/esp1/status"

# === MQTT ===
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT connected:", rc)
    client.subscribe(TOPIC_STATUS)

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print("ESP:", text)
    try:
        # если пришёл статус — шлём в Telegram
        updater.bot.send_message(chat_id=CHAT_ID, text=f"ESP8266: {text}")
    except Exception as e:
        print("TG send error:", e)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()

# === TELEGRAM ===
logging.basicConfig(level=logging.INFO)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я управляю ESP8266. Команды: /on /off /toggle /status")

def on(update: Update, context: CallbackContext):
    mqtt_client.publish(TOPIC_CMD, "on")
    update.message.reply_text("Включаю")

def off(update: Update, context: CallbackContext):
    mqtt_client.publish(TOPIC_CMD, "off")
    update.message.reply_text("Выключаю")

def toggle(update: Update, context: CallbackContext):
    mqtt_client.publish(TOPIC_CMD, "toggle")
    update.message.reply_text("Переключаю")

def gett(update: Update, context: CallbackContext):
    mqtt_client.publish(TOPIC_CMD, "gett")
    update.message.reply_text("Отправляю инфу в ТГ бот")

def status(update: Update, context: CallbackContext):
    update.message.reply_text("Запрашиваю статус...")
    mqtt_client.publish(TOPIC_CMD, "status")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("on", on))
dispatcher.add_handler(CommandHandler("off", off))
dispatcher.add_handler(CommandHandler("toggle", toggle))
dispatcher.add_handler(CommandHandler("gett", gett))
dispatcher.add_handler(CommandHandler("status", status))

print("Бот запущен!")
updater.start_polling()
updater.idle()
