from flask import Flask, jsonify, request, send_file
from security_scanner import perform_full_scan
from recommender import generate_recommendations
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configuration from environment variables set in run.sh
PORT = int(os.environ.get("PORT", 5000))
CLOUDFLARE_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_DOMAIN = os.environ.get("CLOUDFLARE_DOMAIN", "localhost")
DUCKDNS_DOMAIN = os.environ.get("DUCKDNS_DOMAIN", "")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "/config/configuration.yaml")
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    """Run security scan and return results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = perform_full_scan(
        CLOUDFLARE_DOMAIN,
        CLOUDFLARE_API_TOKEN,
        duckdns_domain=DUCKDNS_DOMAIN,
        config_path=CONFIG_PATH,
    )
    recommendations = generate_recommendations(results)
    report = {"scan": results, "recommendations": recommendations}
    json_file = os.path.join(LOG_DIR, f"scan_{timestamp}.json")
    with open(json_file, "w") as f:
        json.dump(report, f)
    logger.info("Scan completed", extra={"results": results})
    return jsonify(report)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        return jsonify({"message": "Configuration updated."})
    return jsonify({"port": PORT, "use_ingress": True})

@app.route('/report', methods=['GET'])
def report():
    """Download the most recent log or scan result."""
    files = [
        os.path.join(LOG_DIR, f)
        for f in os.listdir(LOG_DIR)
        if f.endswith('.json') or f.endswith('.log')
    ]
    if not files:
        return jsonify({"error": "No reports available."}), 404
    latest_file = max(files, key=os.path.getmtime)
    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

