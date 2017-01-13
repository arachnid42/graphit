from app import app
from flask import render_template
from app.core.json_assembler import *
from app.core.facility_handler import *

@app.route('/')
@app.route('/index')
def index():
    fh = JSONAssembler(app.root_path+'/core/config.json')
    fh.get_viz_json()

    return render_template('index.html')