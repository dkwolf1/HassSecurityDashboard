#!/usr/bin/with-contenv bashio
export FLASK_APP=back/app.py
flask run --host=0.0.0.0 --port=$(bashio::config 'port')