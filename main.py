import asyncio
import logging
import paho.mqtt.client as mqtt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '8119566961:AAGpJE-6pT1vyqwL7sEBqzNJZBDa7MCDxwk'
CHAT_ID = '5033674020'

MQTT_BROKER = "broker.hivemq.com"
TOPIC_CMD = "home/esp1/cmd"
TOPIC_STATUS = "home/esp1/status"

# === MQTT ===
mqtt_client = mqtt.Client()

app = ApplicationBuilder().token(TOKEN).build()

async def send_telegram_message(text: str):
    try:
        await app.bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print("TG send error:", e)

def on_connect(client, userdata, flags, rc):
    print("MQTT connected:", rc)
    client.subscribe(TOPIC_STATUS)

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print("ESP:", text)
    # Запускаем асинхронную отправку в Te
