from app import app
from flask import render_template
from app.core.json_assembler import *
from app.core.facility_handler import *

@app.route('/')
@app.route('/index')
def index():
    fh = JSONAssembler(app.root_path+'/core/config.json')
    fh.get_viz_json()
    fac = fh.get_next_craft_optimization_step()
    ffh = FacilityHandler(app.root_path+'/core/config.json', facility_instance=fac)

    return render_template('index.html')