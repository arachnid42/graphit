from app import app
from flask import render_template
from app.core.facility_handler import *

@app.route('/')
@app.route('/index')
def index():
    fh = FacilityHandler(app.root_path + '/core/config.json')
    return render_template('index.html')