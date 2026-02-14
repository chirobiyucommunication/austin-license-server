from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DB_FILE = "licenses.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/register", methods=["POST"])
def register():
    device_id = request.json.get("device_id")
    db = load_db()

    if device_id not in db:
        db[device_id] = {"activated": False}
        save_db(db)

    return jsonify({"status": "registered"})

@app.route("/activate", methods=["POST"])
def activate():
    device_id = request.json.get("device_id")
    db = load_db()

    if device_id not in db:
        return jsonify({"status": "not_found"})

    db[device_id]["activated"] = True
    save_db(db)

    return jsonify({"status": "activated"})

@app.route("/check/<device_id>")
def check(device_id):
    db = load_db()

    if device_id in db and db[device_id]["activated"]:
        return jsonify({"activated": True})

    return jsonify({"activated": False})

if __name__ == "__main__":
    app.run()
