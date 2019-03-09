from flask import Blueprint, render_template, redirect, url_for, \
request, flash, g, jsonify, abort, Response
from jinja2 import TemplateNotFound
import json
from main import db, Area, AdminRegion

api_module = Blueprint('api', __name__, url_prefix='/api')

@api_module.route('/menu/')
def menu():
	node = request.args.get('id')
	node_type = request.args.get('type')
	if node == '#':
		with open(api_module.root_path + '/static/menu_root.json', 'r') as f:
			menu_root = json.load(f)
		return Response(json.dumps(menu_root), mimetype='application/json')
	elif node_type == 'admin':
		if node = '#':
			results = db.session.query(AdminRegion.id, AdminRegion.name).filter()
			response = {}
		pass
	elif node_type == 'layer':
		results = db.session.query(Area.gid, Area.name).filter(Area.type == node)
		leaves = [{'id': str(id), "data": {"type": "poly"}, 'text': name, "state" : { "checkbox_disabled" : True }, "icon": "glyphicon glyphicon-file glyphicon-tree-conifer"} for id, name in results]
		return Response(json.dumps(leaves), mimetype='application/json')

@api_module.route('/shape/')
def shape_info():
	node = request.args.get('id')
	area = Area.query.get(node)
	centroid_area = json.loads(db.session.query(Area.geom.ST_Centroid().ST_AsGeoJSON()).filter(Area.gid == node).first()[0])['coordinates']
	response = {'id': str(area.gid), 'name': area.name, 'type': area.type, 'sous_type': area.sous_type, 'resp': area.resp, 'uicn': area.uicn, 'date_cr': area.date_cr, 'area': area.area, 'centroid': centroid_area}
#	with open(api_module.root_path + '/static/poly.json', 'w') as f:
#		json.dump(response, f)
	return Response(json.dumps(response), mimetype='application/json')

@api_module.route('/shape/geom/')
def shape_geom():
	node = request.args.get('id')
#	area = Area.query.get(node)
#	area_geom = json.loads(db.session.query(Area.geom.ST_Transform("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs", 4326).ST_AsGeoJSON()).filter(Area.gid == node).first()[0])
	area_geom = json.loads(db.session.query(Area.geom.ST_AsGeoJSON()).filter(Area.gid == node).first()[0])
	response = {'type': 'Feature', 'geometry': area_geom}
	return Response(json.dumps(response), mimetype='application/json')