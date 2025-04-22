import socket

def check():
    try:
        s = socket.create_connection(("localhost", 1883), timeout=2)
        s.close()
        return {"status": "ok", "log": "Connected to local Mosquitto broker on port 1883"}
    except Exception as e:
        return {"status": "fail", "log": str(e)}