from app import app
from flask import render_template, jsonify
from app.core.json_assembler import *


@app.route('/')
@app.route('/index')
def index():
    get_data()
    return render_template('index.html')


@app.route('/get_data')
def get_data():
    ja = JSONAssembler(app.root_path+'/core/config.json', force_rebuild=True)
    ja.get_viz_json()
    return ja.get_viz_json()
