import asyncio
import paho.mqtt.client as mqtt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# --- CONFIG ---
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

MQTT_BROKER = "broker.hivemq.com"
TOPIC_CMD = "home/esp1/cmd"
TOPIC_STATUS = "home/esp1/status"

# --- MQTT CLIENT ---
mqtt_client = mqtt.Client()

# --- TELEGRAM ---
app = ApplicationBuilder().token(TG_TOKEN).build()


# ============= MQTT CALLBACKS =============
def on_connect(client, userdata, flags, rc):
    print("MQTT connected:", rc)
    client.subscribe(TOPIC_STATUS)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("ESP:", payload)
    asyncio.run(send_tg(f"📡 ESP сообщает: {payload}"))


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


# ============= TELEGRAM SEND =============
async def send_tg(text):
    try:
        await app.bot.send_message(CHAT_ID, text)
    except Exception as e:
        print("Telegram send error:", e)


# ============= TELEGRAM COMMANDS =============
async def cmd_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mqtt_client.publish(TOPIC_CMD, "on")
    await update.message.reply_text("LED → ON")


async def cmd_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mqtt_client.publish(TOPIC_CMD, "off")
    await update.message.reply_text("LED → OFF")


async def cmd_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mqtt_client.publish(TOPIC_CMD, "toggle")
    await update.message.reply_text("LED → TOGGLE")


async def cmd_temp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mqtt_client.publish(TOPIC_CMD, "gett")   # твоя команда gett
    await update.message.reply_text("📡 Запрашиваю температуру…" )


app.add_handler(CommandHandler("on", cmd_on))
app.add_handler(CommandHandler("off", cmd_off))
app.add_handler(CommandHandler("toggle", cmd_toggle))
app.add_handler(CommandHandler("temp", cmd_temp))


# ================== MAIN ==================
async def main():
    # MQTT
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()

    # Telegram
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("BOT + MQTT started!")
    await asyncio.Event().wait()


asyncio.run(main())
