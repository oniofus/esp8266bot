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
    asyncio.run(send_telegram_message("ESP: " + text))

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


# === Telegram commands ===

async def cmd_led_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mqtt_client.publish(TOPIC_CMD, "LED_ON")
    await update.message.reply_text("→ LED_ON отправлено")

async def cmd_led_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mqtt_client.publish(TOPIC_CMD, "LED_OFF")
    await update.message.reply_text("→ LED_OFF отправлено")

app.add_handler(CommandHandler("on", cmd_led_on))
app.add_handler(CommandHandler("off", cmd_led_off))

# === MAIN ===
async def main():
    print("Starting MQTT…")
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()

    print("Starting Telegram bot…")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()  # never exit

asyncio.run(main())

