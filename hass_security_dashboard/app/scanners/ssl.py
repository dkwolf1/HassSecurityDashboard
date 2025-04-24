import ssl, socket
from datetime import datetime
def check():
    try:
        host = 'google.com'
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=5) as s:
            with ctx.wrap_socket(s, server_hostname=host) as ss:
                cert = ss.getpeercert()
                days = (datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z') - datetime.utcnow()).days
                return {"status": "ok" if days > 7 else "warning", "log": f'SSL valid {days}d'}
    except Exception as e:
        return {"status": "fail", "log": str(e)}