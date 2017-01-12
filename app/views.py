from app import app
from flask import render_template, jsonify
import json
@app.route('/')
@app.route('/index')
def index():
    get_data
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    with open("app/data/factory_layout.json") as json_data:
        return jsonify(json.load(json_data))