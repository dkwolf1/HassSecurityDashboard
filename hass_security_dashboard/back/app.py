from flask import Flask, jsonify, request, send_file, abort
from security_scanner import perform_full_scan
from recommender import generate_recommendations
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configuration from environment variables set in run.sh
PORT = int(os.environ.get("PORT", 5000))
CLOUDFLARE_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_DOMAIN = os.environ.get("CLOUDFLARE_DOMAIN", "localhost")
DUCKDNS_DOMAIN = os.environ.get("DUCKDNS_DOMAIN", "")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "/config/configuration.yaml")

# Directory to store scan logs
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Path to the most recent log file
LATEST_LOG = None

logger = logging.getLogger("scanner")


def setup_logging():
    """Configure logging to a timestamped file for each scan."""
    global LATEST_LOG
    # Remove previous handlers
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    log_path = os.path.join(LOG_DIR, f"scan-{timestamp}.log")
    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    LATEST_LOG = log_path


@app.route('/scan', methods=['POST'])
def scan():
    """Run security scan and return results."""
    setup_logging()
    logger.info("Starting security scan")
    results = perform_full_scan(
        CLOUDFLARE_DOMAIN,
        CLOUDFLARE_API_TOKEN,
        duckdns_domain=DUCKDNS_DOMAIN,
        config_path=CONFIG_PATH,
    )
    # Log individual scan results
    logger.info("Open ports: %s", results.get("open_ports"))
    logger.info("SSL days left: %s", results.get("ssl_days_left"))
    logger.info("MQTT secure: %s", results.get("mqtt_secure"))
    logger.info("Cloudflare protected: %s", results.get("cloudflare_protected"))
    logger.info("DuckDNS match: %s", results.get("duckdns_match"))
    logger.info("Config security: %s", results.get("config_security"))
    logger.info("SSH add-on running: %s", results.get("ssh_addon_running"))
    recommendations = generate_recommendations(results)
    logger.info("Recommendations: %s", recommendations)
    logger.info("Scan complete; log stored at %s", LATEST_LOG)
    return jsonify({"scan": results, "recommendations": recommendations})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"})


@app.route('/report', methods=['GET'])
def report():
    """Return the most recent scan log as a downloadable file."""
    if LATEST_LOG and os.path.exists(LATEST_LOG):
        return send_file(LATEST_LOG, as_attachment=True)
    abort(404)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        return jsonify({"message": "Configuration updated."})
    return jsonify({"port": PORT, "use_ingress": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

