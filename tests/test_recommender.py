import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "hass_security_dashboard", "back"))

from hass_security_dashboard.back import recommender


def test_generate_recommendations():
    results = {
        'ssl_days_left': 10,
        'open_ports': [22],
        'mqtt_secure': False,
        'cloudflare_protected': False
    }
    recs = recommender.generate_recommendations(results)
    assert "Renew SSL certificate soon." in recs
    assert any("Restrict SSH" in r for r in recs)
    assert any("Secure your MQTT" in r for r in recs)
    assert any("Enable Cloudflare" in r for r in recs)
