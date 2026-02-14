from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------- CONFIG ----------------
# Only used for signal bot
SIGNAL_LOG = "signals.json"

# ---------------- DATABASE ----------------
def load_signals():
    try:
        with open(SIGNAL_LOG, "r") as f:
            return json.load(f)
    except:
        return []

def save_signals(data):
    with open(SIGNAL_LOG, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- SIGNAL ENDPOINT ----------------
@app.route("/signal", methods=["POST"])
def receive_signal():
    data = request.json

    # Validate required fields
    required = ["pair", "direction", "timeframe", "strength"]
    if not all(field in data for field in required):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Save the signal
    signals = load_signals()
    signals.append(data)
    save_signals(signals)

    print(f"New signal received: {data}")
    return jsonify({"status": "success", "message": "Signal received"}), 200

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    print("Signal bot running on port 5001...")
    app.run(host="0.0.0.0", port=5001)
