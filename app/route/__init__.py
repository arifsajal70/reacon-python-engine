# Import Helpers
from app.helpers.dict import AttrDict

# Define route list
routes = dict(
    api=list()
)


def register(endpoint, view_func, methods=None, name=None, to='api', prefix=None):
    """
    Api Route Registration
    :param endpoint, view_func, methods, name, to:
    :type endpoint: str
    :type view_func: () -> Any
    :type methods: list
    :type name: str
    :type prefix: str
    :type to: str
    :return:
    """
    if methods is None:
        methods = ['GET', 'POST']

    routes[to].append(AttrDict(dict(
        name=name,
        endpoint=endpoint,
        view_func=view_func,
        methods=methods,
        prefix=prefix
    )))


def get_routes(frm='api'):
    """
    Get Defined Api routes
    :param frm:
    :type frm: str
    :return routes
    :rtype routes: list
    """
    from .api import register_api_endpoints
    register_api_endpoints()

    return routes[frm]
