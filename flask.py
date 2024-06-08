from flask import Flask, render_template, jsonify, request
from agent import run_conversation  # Ensure this module is available and correctly implemented

app = Flask(__name__)

@app.route("/process_message", methods=["POST"])
def process_message_func1():
    msg = request.json.get("message")
    if not msg:
        return jsonify({"response": "No message provided"}), 400
    print("Received message:", msg)
    resp = run_conversation(msg)
    return jsonify({"response": resp})

@app.route("/")
def index():
    return render_template("index.html")  # Corrected template filename

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
