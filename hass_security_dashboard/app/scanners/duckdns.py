import requests, socket

def check():
    domain = "yourdomain.duckdns.org"
    try:
        external_ip = requests.get("https://api.ipify.org").text.strip()
        resolved_ip = socket.gethostbyname(domain)
        match = external_ip == resolved_ip
        return {
            "status": "ok" if match else "warning",
            "log": f"DuckDNS {domain} resolved to {resolved_ip}, external IP is {external_ip}"
        }
    except Exception as e:
        return {"status": "fail", "log": str(e)}