from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hass Security Dashboard is running</h1>"

@app.route("/api/status")
def status():
    return jsonify({"status": "online"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
