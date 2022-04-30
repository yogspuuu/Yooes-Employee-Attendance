import json
from api import db, app
from flask.views import MethodView
# from api.catalog.models import Product
from flask import request, jsonify, Blueprint, abort

recognition = Blueprint('catalog', __name__)

@recognition.route('/')
@recognition.route('/home')
def home():
    return "Yooes recognition api."
