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
    fh =JSONAssembler(app.root_path+'/core/config.json')
    fh.get_viz_json()
    return fh.get_viz_json()
