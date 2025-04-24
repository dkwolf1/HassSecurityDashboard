from flask import Flask, jsonify, send_from_directory
from waitress import serve
import os, importlib, traceback

app = Flask(__name__)
scanner_path = "/app/scanners"

@app.route("/")
def index():
    return send_from_directory("/app/web", "index.html")

@app.route("/api/status")
def status():
    results = {}
    for fname in os.listdir(scanner_path):
        if fname.endswith(".py"):
            key = fname[:-3]
            try:
                mod = importlib.import_module(f"scanners.{key}")
                res = mod.run()
                results[key] = {"status": res.get("status", "unknown"), "log": res.get("log", "")}
            except Exception as e:
                results[key] = {"status": "fail", "log": traceback.format_exc()}
    return jsonify(results)

@app.route("/api/logs/<scanner>")
def logs(scanner):
    try:
        mod = importlib.import_module(f"scanners.{scanner}")
        res = mod.run()
        return res.get("log", ""), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return f"Error: {e}", 500

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("/app/web", filename)

if __name__ == "__main__":
    print("✅ Security Dashboard server running on 0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)