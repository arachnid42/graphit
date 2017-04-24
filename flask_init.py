#! /usr/bin/env python3

from app import app
import json

# determine what port to start on
with open("vconf.json") as cf:
    port = json.load(cf.read())['forward_ports']['guest']

# start flask
app.run(host='0.0.0.0', port=port, debug=True)
