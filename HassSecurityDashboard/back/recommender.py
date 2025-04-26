def generate_recommendations(scan_results):
    recs = []
    if scan_results.get("ssl_days_left", 0) < 30:
        recs.append("Renew SSL certificate soon.")
    if 22 in scan_results.get("open_ports", []):
        recs.append("Restrict SSH access or change the default port.")
    if not scan_results.get("mqtt_secure", True):
        recs.append("Secure your MQTT broker with authentication and TLS.")
    if not scan_results.get("cloudflare_protected", False):
        recs.append("Enable Cloudflare proxy for external traffic.")
    return recs