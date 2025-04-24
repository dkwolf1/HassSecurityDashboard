import subprocess
def check():
    try:
        result = subprocess.check_output(["ha", "addons", "info", "core_ssh"], text=True)
        return {"status": "ok", "log": result}
    except Exception as e:
        return {"status": "fail", "log": str(e)}