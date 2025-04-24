import subprocess
def check():
    try:
        result = subprocess.check_output(["ss", "-tuln"], text=True)
        return {"status": "ok", "log": result}
    except Exception as e:
        return {"status": "fail", "log": str(e)}