from flask import Flask, jsonify, request
from security_scanner import perform_full_scan
from recommender import generate_recommendations

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    results = perform_full_scan()
    recommendations = generate_recommendations(results)
    return jsonify({"scan": results, "recommendations": recommendations})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        return jsonify({"message": "Configuration updated."})
    return jsonify({"port": 5000, "use_ingress": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)