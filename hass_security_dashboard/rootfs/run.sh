#!/usr/bin/with-contenv bash
set -e

# Kies tussen ingress of standalone HTTP
if [ "${USE_INGRESS}" = "false" ]; then
  export FLASK_RUN_PORT=${PORT:-8123}
  flask --app /app/dashboard run --host 0.0.0.0
else
  # Ingress-mode: alleen localhost, HA-supervisor regelt TLS/HTTPS
  export FLASK_RUN_PORT=8123
  flask --app /app/dashboard run --host 127.0.0.1
fi
