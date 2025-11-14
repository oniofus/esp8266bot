import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------------------
# Состояние устройства
# ---------------------------
device_state = {"on": False}  # False = выключено, True = включено

# ---------------------------
# Хендлеры команд
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ваш ESP8266 Telegram бот. Используй команды /on и /off."
    )

async def turn_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    device_state["on"] = True
    await update.message.reply_text("✅ Устройство включено!")

async def turn_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    device_state["on"] = False
    await update.message.reply_text("❌ Устройство выключено!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_text = "включено ✅" if device_state["on"] else "выключено ❌"
    await update.message.reply_text(f"Состояние устройства: {state_text}")

# ---------------------------
# Исправляем Application для Python 3.13
# ---------------------------
class MyApplication(ApplicationBuilder):
    def build(self):
        app = super().build()
        if not hasattr(app, "_Application__stop_running_marker"):
            app._Application__stop_running_marker = asyncio.Event()
        return app

# ---------------------------
# Токен бота
# ---------------------------
import os
TG_TOKEN = os.getenv("TG_TOKEN")  # Брать из Render env vars

# ---------------------------
# Создаем приложение
# ---------------------------
app = MyApplication().token(TG_TOKEN).build()

# Добавляем команды
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("on", turn_on))
app.add_handler(CommandHandler("off", turn_off))
app.add_handler(CommandHandler("status", status))

# ---------------------------
# Запуск бота
# ---------------------------
if __name__ == "__main__":
    app.run_polling()


