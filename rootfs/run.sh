#!/usr/bin/with-contenv bash
# Start security-dashboard service
if [ "${USE_INGRESS}" = "false" ]; then
  export FLASK_RUN_PORT=${PORT:-8123}
  flask --app /app/dashboard run --host 0.0.0.0
else
  # Ingress mode: app draait op localhost:8123
  export FLASK_RUN_PORT=8123
  flask --app /app/dashboard run --host 127.0.0.1
fi