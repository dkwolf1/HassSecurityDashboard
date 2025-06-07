#!/usr/bin/with-contenv bashio
export FLASK_APP=back/app.py

# Read options from Hass.io configuration or environment variables
export PORT="${PORT:-$(bashio::config 'port')}"
export USE_INGRESS="${USE_INGRESS:-$(bashio::config 'use_ingress')}"
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-$(bashio::config 'cloudflare_api_token')}"

flask run --host=0.0.0.0 --port="${PORT}"
