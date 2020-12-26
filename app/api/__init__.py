# Import Flask Things
from flask import Blueprint

# Import routes
from app.route.api import fire_routes as fire_api_routes

api = Blueprint('data', __name__)

fire_api_routes(api)
