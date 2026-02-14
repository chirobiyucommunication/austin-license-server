# server.py
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DB_FILE = "licenses.json"

# ---------------- DB Helpers ----------------
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- Register Device ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    device_id = data.get("device_id")
    db = load_db()

    if not device_id:
        return jsonify({"status": "error", "message": "Missing device_id"}), 400

    if device_id not in db:
        db[device_id] = {"activated": False}
        save_db(db)

    return jsonify({"status": "registered"})

# ---------------- Activate Device ----------------
@app.route("/activate", methods=["POST"])
def activate():
    data = request.json
    device_id = data.get("device_id")
    db = load_db()

    if device_id not in db:
        return jsonify({"status": "not_found"}), 404

    db[device_id]["activated"] = True
    save_db(db)
    return jsonify({"status": "activated"})

# ---------------- Check Activation ----------------
@app.route("/check/<device_id>")
def check(device_id):
    db = load_db()
    if device_id in db and db[device_id]["activated"]:
        return jsonify({"activated": True})
    return jsonify({"activated": False})

if __name__ == "__main__":
    # Use host="0.0.0.0" if deploying to Render / VPS
    app.run(host="0.0.0.0", port=5000)
