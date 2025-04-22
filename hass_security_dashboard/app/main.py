from flask import Flask, jsonify, send_from_directory
from scanners import ports, ssl, duckdns, cloudflare, mosquitto, ssh, ha_config
import os

app = Flask(__name__, static_folder="web")

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "ports": ports.check(),
        "ssl": ssl.check(),
        "duckdns": duckdns.check(),
        "cloudflare": cloudflare.check(),
        "mosquitto": mosquitto.check(),
        "ssh": ssh.check(),
        "ha_config": ha_config.check()
    })

@app.route("/api/logs/<scanner>")
def logs(scanner):
    log_path = f"/app/logs/{scanner}.log"
    if os.path.exists(log_path):
        with open(log_path) as f:
            return f.read(), 200, {'Content-Type': 'text/plain'}
    return "Log not found", 404