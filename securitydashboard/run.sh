#!/usr/bin/with-contenv bashio

PORT=$(bashio::config 'port')
CLOUDFLARE_TOKEN=$(bashio::config 'cloudflare_token')

export PORT
export CLOUDFLARE_TOKEN

echo "[INFO] Starting Hass Security Dashboard on port ${PORT}"
python3 /usr/local/bin/app.py
