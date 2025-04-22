import ssl, socket
from datetime import datetime

def check():
    try:
        hostname = "google.com"
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expires = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days = (expires - datetime.utcnow()).days
                return {
                    "status": "ok" if days > 7 else "warning",
                    "log": f"SSL cert for {hostname} valid for {days} more days."
                }
    except Exception as e:
        return {"status": "fail", "log": str(e)}