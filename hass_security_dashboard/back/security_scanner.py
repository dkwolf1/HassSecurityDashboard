import socket
import ssl
import datetime
import requests

def scan_open_ports(host='localhost', ports=[22, 80, 443, 1883, 8883]):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                s.connect((host, port))
                open_ports.append(port)
            except (socket.timeout, ConnectionRefusedError):
                pass
    return open_ports

def check_ssl_certificate(hostname):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=hostname) as conn:
            conn.settimeout(3.0)
            conn.connect((hostname, 443))
            cert = conn.getpeercert()
            expiry = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_left = (expiry - datetime.datetime.utcnow()).days
            return days_left
    except Exception as e:
        print(f"SSL check failed: {e}")
        return None

def check_mqtt_security(host='localhost', port=1883):
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect(host, port, 60)
        client.loop_start()
        client.disconnect()
        return False
    except Exception:
        return True

def check_cloudflare(domain, api_token):
    try:
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        zone_resp = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers)
        zones = zone_resp.json()["result"]
        for zone in zones:
            if domain.endswith(zone["name"]):
                return True
        return False
    except Exception as e:
        print(f"Cloudflare check failed: {e}")
        return None

def perform_full_scan(domain, api_token):
    host = 'localhost'
    open_ports = scan_open_ports(host)
    ssl_days_left = check_ssl_certificate(host)
    mqtt_secure = check_mqtt_security(host)

    cloudflare_protected = False
    if api_token and domain:
        result = check_cloudflare(domain, api_token)
        if result is not None:
            cloudflare_protected = result

    return {
        "open_ports": open_ports,
        "ssl_days_left": ssl_days_left,
        "mqtt_secure": mqtt_secure,
        "cloudflare_protected": cloudflare_protected
    }
