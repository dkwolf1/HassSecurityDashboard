import socket
import ssl
import datetime
import requests
import yaml
import logging

from ha_cli_utils import get_addon_info, get_core_info

logger = logging.getLogger(__name__)

def scan_open_ports(host='localhost', ports=[22, 80, 443, 1883, 8883]):
    logger.info("Scanning open ports on %s", host)
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                s.connect((host, port))
                open_ports.append(port)
            except (socket.timeout, ConnectionRefusedError):
                pass
    logger.info("Open ports found: %s", open_ports)
    return open_ports

def check_ssl_certificate(hostname):
    logger.info("Checking SSL certificate for %s", hostname)
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
        logger.warning("SSL check failed: %s", e)
        return None

def check_mqtt_security(host='localhost', port=1883):
    logger.info("Checking MQTT security on %s:%s", host, port)
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect(host, port, 60)
        client.loop_start()
        client.disconnect()
        return False
    except Exception as e:
        logger.info("MQTT connection failed: %s", e)
        return True

def check_cloudflare(domain, api_token):
    logger.info("Verifying Cloudflare for %s", domain)
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
        logger.warning("Cloudflare check failed: %s", e)
        return None

def check_duckdns(domain):
    """Verify DuckDNS domain resolves to current public IP."""
    logger.info("Verifying DuckDNS domain %s", domain)
    try:
        public_ip = requests.get("https://api.ipify.org").text.strip()
        resolved_ip = socket.gethostbyname(domain)
        return public_ip == resolved_ip
    except Exception as e:
        logger.warning("DuckDNS check failed: %s", e)
        return None

def parse_configuration(path):
    """Parse configuration.yaml and flag insecure settings."""
    logger.info("Parsing configuration %s", path)
    results = {
        "http_ssl": True,
        "mqtt_has_password": True,
    }
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        http_cfg = data.get("http", {}) or {}
        if not http_cfg.get("ssl_certificate"):
            results["http_ssl"] = False
        mqtt_cfg = data.get("mqtt", {}) or {}
        if isinstance(mqtt_cfg, dict) and not mqtt_cfg.get("password"):
            results["mqtt_has_password"] = False
    except Exception as e:
        logger.warning("Config parse failed: %s", e)
        results["error"] = str(e)
    return results

def get_ssh_addon_details():
    """Return details of the SSH add-on using the HA CLI."""
    info = get_addon_info("core_ssh")
    if info is None:
        return None
    return {
        "running": info.get("state") == "started",
        "version": info.get("version"),
        "update_available": info.get("update_available"),
    }

def perform_full_scan(domain, api_token, duckdns_domain=None, config_path=None):
    logger.info("Starting full scan")
    host = "localhost"
    open_ports = scan_open_ports(host)
    ssl_days_left = check_ssl_certificate(host)
    mqtt_secure = check_mqtt_security(host)

    cloudflare_protected = False
    if api_token and domain:
        result = check_cloudflare(domain, api_token)
        if result is not None:
            cloudflare_protected = result

    duckdns_ok = None
    if duckdns_domain:
        duckdns_ok = check_duckdns(duckdns_domain)

    config_security = {}
    if config_path:
        config_security = parse_configuration(config_path)

    ssh_addon = get_ssh_addon_details()
    core_info = get_core_info()
    logger.info("Scan finished")

    results = {
        "open_ports": open_ports,
        "ssl_days_left": ssl_days_left,
        "mqtt_secure": mqtt_secure,
        "cloudflare_protected": cloudflare_protected,
        "duckdns_match": duckdns_ok,
        "config_security": config_security,
        "ssh_addon": ssh_addon,
        "core": core_info,
    }
    logger.debug("Scan results: %s", results)
    return results
