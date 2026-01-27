from flask import Blueprint
from flask import jsonify
from flask import request
from core_logic import attendance_chain, save_chain



# create a blueprint

# create a blueprint for the routes
attendence_bp = Blueprint('atendence_app', __name__)




@attendence_bp.route("/")
def home():
    return "📘 Attendance Blockchain Running!"

@attendence_bp.route("/add", methods=["POST"])
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

@attendence_bp.route("/chain", methods=["GET"])
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

@attendence_bp.route("/history/<student>", methods=["GET"])
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
