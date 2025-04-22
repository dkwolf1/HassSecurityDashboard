import yaml

def check():
    try:
        with open("/config/configuration.yaml") as f:
            config = yaml.safe_load(f)
        issues = []
        if "http" not in config:
            issues.append("Missing http section")
        return {"status": "ok" if not issues else "warning", "log": "\n".join(issues) or "Config looks good"}
    except Exception as e:
        return {"status": "fail", "log": str(e)}