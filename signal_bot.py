import telebot
from flask import Flask, request, jsonify
import threading
import json
import os

# ---------------- CONFIG ----------------
SIGNAL_BOT_TOKEN = "8534924197:AAFq8W69GWlcYGKUAySzzbeEFMYooVNSpZI"
CHANNEL_USERNAME = "@AustinTradeSignals"
DB_FILE = "users_db.json"  # Use the same file your admin bot updates

bot = telebot.TeleBot(SIGNAL_BOT_TOKEN)
app = Flask(__name__)

# ---------------- DATABASE ----------------
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

# ---------------- POST SIGNAL TO CHANNEL ----------------
def post_signal_to_channel(message):
    try:
        bot.send_message(CHANNEL_USERNAME, message)
        print(f"✅ Signal posted to {CHANNEL_USERNAME}")
    except Exception as e:
        print("❌ Failed to post signal:", e)

# ---------------- SEND TRADE TO CLIENTS ----------------
def send_trade_to_clients(signal):
    db = load_db()
    for device_id, info in db.items():
        if info.get("activated"):
            chat_id = info.get("chat_id")
            try:
                bot.send_message(chat_id, f"/trade {signal}")
                print(f"✅ Sent trade to {device_id}")
            except Exception as e:
                print(f"❌ Failed to send trade to {device_id}: {e}")

# ---------------- TRADINGVIEW WEBHOOK ----------------
@app.route("/signal", methods=["POST"])
def receive_signal():
    data = request.json
    pair = data.get("pair")
    side = data.get("side")
    timeframe = data.get("timeframe")
    strength = data.get("strength")

    if strength != "strong":
        return jsonify({"status":"ignored"})

    # Format the message
    signal_message = f"📊 New Signal:\nPair: {pair}\nSide: {side}\nTimeframe: {timeframe}\n⚡ Strong Trend"

    # Send to Telegram channel
    post_signal_to_channel(signal_message)

    # Send trade command to all active clients
    send_trade_to_clients(f"{pair} {side} {timeframe}")

    return jsonify({"status":"ok"})

# ---------------- RUN TELEGRAM BOT ----------------
def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot, daemon=True).start()

# ---------------- RUN FLASK SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
