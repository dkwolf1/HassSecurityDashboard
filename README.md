## 🛡️ Hass Security Dashboard ( UNDER DEVELOPMENT) 

**A powerful security auditing add-on for Home Assistant OS with a graphical interface.**

This add-on scans your Home Assistant server and ecosystem for security vulnerabilities and best practices. It provides a clear dashboard showing which areas are secure, misconfigured, or exposed.

### 🔍 Features
- 🔓 Open port scanner (detects exposed or unknown ports)
- 🔐 SSL certificate check (expiration & HTTPS detection)
- 🌐 DuckDNS domain reachability and IP match
- ☁️ Cloudflare DNS record & proxy status (via optional API token)
- 📡 Mosquitto MQTT broker security validation (TLS & anonymous access)
- 🧩 Home Assistant config security parser (`configuration.yaml`)
- 🖥️ SSH terminal add-on check (auth & exposure)
- 🌐 Web-based interface with multilingual support (🇬🇧 English / 🇳🇱 Dutch)
  - Use the language selector at the top of the dashboard to switch translations
- 📝 Per-module logs + downloadable full report

### 🧠 Built with
- Python 3.11
- Flask (backend)
- HTML/JS frontend
- Docker (Supervisor compatible)
- HA CLI integration (`ha addons info`)

---

### 🛠️ Requirements
- Home Assistant OS (Supervisor access required)
- Network access (`host`) + privileges (`NET_ADMIN`)
- Optional: Cloudflare API token

### Configuration Options
Edit `config.json` or the add-on options in Home Assistant:

- `cloudflare_api_token` – API token for checking Cloudflare protection.
- `cloudflare_domain` – Domain served via Cloudflare to verify and use for SSL checks.
- `duckdns_domain` – DuckDNS hostname to verify against your public IP.
- `config_path` – Path to `configuration.yaml` for security parsing.

> Use this tool to secure your smart home before attackers try to.


### Running tests
Use `pytest` to run the test suite:

```bash
pytest
```

### Troubleshooting
If the Docker build fails while installing Python packages, ensure build
dependencies are present. The Dockerfile now installs `gcc`, `musl-dev`,
`python3-dev`, and `libffi-dev` before running `pip3 install`.

