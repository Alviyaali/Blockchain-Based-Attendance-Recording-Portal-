from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain_1 import Blockchain, Block
import json
import os
from time import time

app = Flask(__name__)
CORS(app)

SAVE_FILE = "attendance_data.json"

# Initialize blockchain
attendance_chain = Blockchain()
if not hasattr(attendance_chain, "attendance_log") or attendance_chain.attendance_log is None:
    attendance_chain.attendance_log = {}

# -------------------- Load blockchain from JSON --------------------
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        try:
            saved = json.load(f)
        except json.JSONDecodeError:
            saved = []

    if saved:  # rebuild chain only if JSON has blocks
        attendance_chain.chain = []
        for b in saved:
            block = Block(b["index"], b["timestamp"], b["data"], b["previous_hash"])
            block.hash = b["hash"]
            attendance_chain.chain.append(block)

        # Rebuild attendance_log
        attendance_chain.attendance_log = {}
        for block in attendance_chain.chain:
            if isinstance(block.data, dict):
                student = block.data.get("student")
                date = block.data.get("date")
                if student and date:
                    key = f"{student}-{date}"
                    attendance_chain.attendance_log[key] = True
else:
    # Create empty JSON if not exists
    with open(SAVE_FILE, "w") as f:
        json.dump([], f)

# -------------------- Save blockchain to JSON --------------------
def save_chain():
    data_list = []
    for block in attendance_chain.chain:
        data_list.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    with open(SAVE_FILE, "w") as f:
        json.dump(data_list, f, indent=4)

# -------------------- Routes --------------------
@app.route("/")
def home():
    return "📘 Attendance Blockchain Running!"

@app.route("/add", methods=["POST"])
def add_block():
    data = request.get_json()
    print("Incoming data from HTML:", data)  # debug

    required_keys = ["student", "date", "time", "status"]
    for key in required_keys:
        if key not in data or not str(data[key]).strip():
            print(f"Missing or empty field: {key}")
            return jsonify({"error": f"Missing or empty field: {key}"}), 400

    if not hasattr(attendance_chain, "attendance_log") or attendance_chain.attendance_log is None:
        attendance_chain.attendance_log = {}

    response, status = attendance_chain.add_block(data)
    print("Add block response:", response, status)  # debug

    if status != 201:
        return jsonify(response), status

    save_chain()
    latest = attendance_chain.get_latest_block()
    return jsonify({
        "message": "Attendance Block Added!",
        "hash": latest.hash,
        "mining_time": response["mining_time"],
        "data": data
    }), 201

@app.route("/chain", methods=["GET"])
def chain():
    output = []
    for block in attendance_chain.chain:
        output.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify(output)

@app.route("/history/<student>", methods=["GET"])
def history(student):
    history_list = []
    for block in attendance_chain.chain:
        if isinstance(block.data, dict) and block.data.get("student") == student:
            history_list.append({
                "index": block.index,
                "date": block.data.get("date"),
                "time": block.data.get("time"),
                "status": block.data.get("status"),
                "hash": block.hash
            })
    return jsonify(history_list)

# -------------------- Run server --------------------
if __name__ == "__main__":
    app.run(debug=True)







