import requests, socket
def check():
 try:
  domain = 'yourdomain.duckdns.org'
  ext = requests.get('https://api.ipify.org').text.strip()
  res = socket.gethostbyname(domain)
  return {'status': 'ok' if ext == res else 'warning', 'log': f'{domain} → {res}, ext IP: {ext}'}
 except Exception as e:
  return {'status': 'fail', 'log': str(e)}