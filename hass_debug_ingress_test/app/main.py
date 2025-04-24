from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)

@app.route("/")
def root():
    return "🟢 Hass Security Dashboard (minimal UI)"

@app.route("/api/debug")
def debug():
    return jsonify({
        "message": "🟢 Backend API bereikbaar",
        "remote_addr": request.remote_addr,
        "headers": dict(request.headers)
    })

if __name__ == "__main__":
    print("🟢 DEBUG MODE: Starting server on 0.0.0.0:5000...")
    serve(app, host="0.0.0.0", port=5000)