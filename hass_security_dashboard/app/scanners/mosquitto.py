import socket
def check():
    try:
        s = socket.create_connection(("localhost", 1883), timeout=2)
        s.close()
        return {"status": "ok", "log": "Mosquitto reachable"}
    except Exception as e:
        return {"status": "fail", "log": str(e)}