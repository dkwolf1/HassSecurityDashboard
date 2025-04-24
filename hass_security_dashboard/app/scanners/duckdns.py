import requests, socket
def check():
    try:
        ext = requests.get('https://api.ipify.org').text.strip()
        dns = socket.gethostbyname('yourdomain.duckdns.org')
        return {"status": "ok" if ext == dns else "warning", "log": f'DNS: {dns}, External: {ext}'}
    except Exception as e:
        return {"status": "fail", "log": str(e)}