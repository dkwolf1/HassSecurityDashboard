from flask import Flask, jsonify, send_from_directory
from scanners import ports, ssl, duckdns, cloudflare, mosquitto, ssh, ha_config
from waitress import serve
import os

app = Flask(__name__, static_folder="web")

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/api/status")
def status():
    try:
        return jsonify({
            "ports": ports.check(),
            "ssl": ssl.check(),
            "duckdns": duckdns.check(),
            "cloudflare": cloudflare.check(),
            "mosquitto": mosquitto.check(),
            "ssh": ssh.check(),
            "ha_config": ha_config.check()
        })
    except Exception as e:
        return jsonify({"status": "fail", "log": str(e)}), 500

@app.route("/api/logs/<scanner>")
def logs(scanner):
    path = f"/app/logs/{scanner}.log"
    if os.path.exists(path):
        with open(path) as f:
            return f.read(), 200, {'Content-Type': 'text/plain'}
    return "Log not found", 404

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)