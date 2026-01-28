import json
import os
from time import time
from blockchain_1 import Blockchain, Block

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

