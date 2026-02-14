from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DB_FILE = "licenses.json"

# ---------------- DATABASE ----------------
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "Austin Maxi Bot License Server Running"

# ---------------- REGISTER DEVICE ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    device_id = data.get("device_id")

    if not device_id:
        return jsonify({"status": "error", "message": "device_id missing"})

    db = load_db()

    if device_id not in db:
        db[device_id] = {"activated": False}
        save_db(db)
        return jsonify({"status": "registered"})

    return jsonify({"status": "already_registered"})

# ---------------- ACTIVATE DEVICE ----------------
@app.route("/activate", methods=["POST"])
def activate():
    data = request.get_json()
    device_id = data.get("device_id")

    db = load_db()

    if device_id not in db:
        return jsonify({"status": "not_found"})

    db[device_id]["activated"] = True
    save_db(db)

    return jsonify({"status": "activated"})

# ---------------- CHECK LICENSE ----------------
@app.route("/check/<device_id>", methods=["GET"])
def check(device_id):
    db = load_db()

    if device_id in db and db[device_id]["activated"]:
        return jsonify({"activated": True})

    return jsonify({"activated": False})

# ---------------- RENDER PORT FIX ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

