from app import app
from flask import render_template, request
from app.core.json_assembler import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/get_data')
def get_data():
    ja = JSONAssembler(app.root_path+'/core/config.json', force_rebuild=True)
    return ja.get_viz_json()


@app.route('/get_data_filtered')
def get_data_filtered():
    dummy_time_1 = " 00:00:00"
    dummy_time_2 = " 23:59:59"
    date_from = request.args.get('start', None, type=str) + dummy_time_1
    date_to = request.args.get('end', None, type=str) + dummy_time_2
    ja = JSONAssembler(app.root_path+'/core/config.json', force_rebuild=True, date_boundaries=[date_from, date_to])
    return ja.get_viz_json()
