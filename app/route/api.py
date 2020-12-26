# Import Route Things
from . import register, get_routes

# Import Api Controller files
from ..api.authentication import login

# Import Flask Things
from flask import Blueprint

to = 'api'


def register_api_endpoints():
    """
    Define All Api Routes Here
    :return:
    """
    register(endpoint='/login', view_func=login, to=to, prefix='auth')


def fire_routes(blueprint):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :return:
    """
    routes = get_routes('api')
    for route in routes:
        blueprint.add_url_rule(route.prefix and f"/{route.prefix}/{route.endpoint}" or route.endpoint,
                               methods=route.methods, view_func=route.view_func)
