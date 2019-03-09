import os
from flask import Flask, g, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import geoalchemy2 as gdb
import logging

app = Flask(__name__, static_url_path=os.path.dirname(os.path.abspath(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qcarta:terreauLib@155.138.209.61/qcarta'
db = SQLAlchemy(app)
#app.secret_key = 'well'
config = {'MAPBOXGL_API_KEY': os.environ['MAPBOXGL_API_KEY']}

if os.environ.get('WSGI_CURRENT', '') == 'gunicorn':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

class Area(db.Model):
	__tablename__ = 'areas'
	gid = db.Column(db.Integer, nullable=False, primary_key=True)
	geom = db.Column(gdb.Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=False)
	name = db.Column(db.String(150))
	type = db.Column(db.String(100))
	sous_type = db.Column(db.String(75))
	resp = db.Column(db.String(254))
	uicn = db.Column(db.String(5))
	date_cr = db.Column(db.DateTime())
	area = db.Column(db.Float())
	id_mrc = db.Column(db.String(3))
	id_reg = db.Column(db.String(2))

class AdminRegion(db.Model):
	__tablename__ = 'admin_regions'
	gid = db.Column(db.Integer, nullable=False, primary_key=True)
	geom = db.Column(gdb.Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=False)
	name = db.Column(db.String(150))
	type = db.Column(db.String(100))
	id = db.Column(db.String(64))
	parent0 = db.Column(db.String(64))
	parent1 = db.Column(db.String(64))
	parent2 = db.Column(db.String(64))
	id_com = db.Column(db.String(3))
	date_cr = db.Column(db.DateTime())
	area = db.Column(db.Float())

@app.context_processor
def inject_in_all_templates():
    return dict(config=config)

from api import api_module
app.register_blueprint(api_module)
api_module.json_encoder = None

@app.route('/')
def index():
	return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)