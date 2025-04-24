import yaml
def check():
    try:
        with open('/config/configuration.yaml') as f:
            yaml.safe_load(f)
        return {"status": "ok", "log": "HA config parsed"}
    except Exception as e:
        return {"status": "fail", "log": str(e)}