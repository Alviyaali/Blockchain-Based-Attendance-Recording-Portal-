from flask import Flask, request, jsonify
from flask_cors import CORS
from routs import attendence_bp

app = Flask(__name__) # Create a Flask app with dunder method
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}) # Only allow requests from http://127.0.0.1:5500 (safety measure)
# Register the blueprint
app.register_blueprint(attendence_bp)

# -------------------- Run server --------------------
if __name__ == "__main__":
    app.run(debug=True)







