# Import Route Things
from . import register, get_routes

# Import Api Controller files
from ..api.authentication import login, logout
from ..api.modules.client import get_clients, get_client

# Import Flask Things
from flask import Blueprint

to = 'api'


def register_api_endpoints():
    """
    Define All Api Routes Here
    :return:
    """
    """Authentication Routes"""
    register(endpoint='/login', view_func=login, to=to, prefix='auth')
    register(endpoint='/logout', view_func=logout, to=to, prefix='auth')

    """Client Module Routes For Admin"""
    register(endpoint='/get-clients', view_func=get_clients, to=to, prefix='admin', methods=['POST'])
    register(endpoint='/get-client/<string:client_id>', view_func=get_client, to=to, prefix='admin', methods=['GET'])


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
