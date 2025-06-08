import os
import json
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(ROOT, "hass_security_dashboard", "config.json")

options = json.load(open(CONFIG_PATH))["options"]

shell_script = f'''
set -e
bashio::config() {{
    case "$1" in
        port) echo "{options['port']}" ;;
        use_ingress) echo "{str(options['use_ingress']).lower()}" ;;
        cloudflare_api_token) echo "{options['cloudflare_api_token']}" ;;
        duckdns_domain) echo "{options['duckdns_domain']}" ;;
        config_path) echo "{options['config_path']}" ;;
    esac
}}
flask() {{
    echo "PORT=$PORT"
    echo "CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN"
    echo "DUCKDNS_DOMAIN=$DUCKDNS_DOMAIN"
    echo "CONFIG_PATH=$CONFIG_PATH"
}}
source hass_security_dashboard/run.sh
'''

result = subprocess.run(['bash', '-c', shell_script], capture_output=True, text=True)
output = dict(line.split('=', 1) for line in result.stdout.strip().splitlines())


def test_run_sh_uses_config_values():
    assert output['PORT'] == str(options['port'])
    assert output['CLOUDFLARE_API_TOKEN'] == options['cloudflare_api_token']
    assert output['DUCKDNS_DOMAIN'] == options['duckdns_domain']
    assert output['CONFIG_PATH'] == options['config_path']
