from flask import Flask, jsonify, request
from security_scanner import perform_full_scan
from recommender import generate_recommendations
import os

app = Flask(__name__)

# Configuration from environment variables set in run.sh
PORT = int(os.environ.get("PORT", 5000))
CLOUDFLARE_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_DOMAIN = os.environ.get("CLOUDFLARE_DOMAIN", "localhost")
DUCKDNS_DOMAIN = os.environ.get("DUCKDNS_DOMAIN", "")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "/config/configuration.yaml")

@app.route('/scan', methods=['POST'])
def scan():
    """Run security scan and return results."""
    results = perform_full_scan(
        CLOUDFLARE_DOMAIN,
        CLOUDFLARE_API_TOKEN,
        duckdns_domain=DUCKDNS_DOMAIN,
        config_path=CONFIG_PATH,
    )
    recommendations = generate_recommendations(results)
    return jsonify({"scan": results, "recommendations": recommendations})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        return jsonify({"message": "Configuration updated."})
    return jsonify({"port": PORT, "use_ingress": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

