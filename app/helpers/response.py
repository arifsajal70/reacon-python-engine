from flask import jsonify
from .session import get_current_session, update_token_expiration


class Response:
    """Default Items For Api Response"""
    session = None
    data = None
    errors = None
    status_code = 200
    message = ''
    status = None
    authenticated = False

    def __init__(self, session=None, status_code=200, message='', status=None, data=None, errors=None, authenticated=False):
        """Setting Constructor Values Received From Initialization"""
        self.session = session
        self.status_code = status_code
        self.message = message
        self.status = status
        self.data = data
        self.errors = errors
        self.authenticated = authenticated

        """Set User If Request is Authenticated"""

        self._get_session()

        """Set Status If No Status Received"""
        if status is None:
            self._set_status()

    def send(self):
        return jsonify(
            {
                "session": self.session,
                "status_code": self.status_code,
                "message": self.message,
                "status": self.status,
                "data": self.data,
                "errors": self.errors,
                "authenticated": self.authenticated,
            }
        ), self.status_code

    def _get_session(self):
        self.session = get_current_session(formatted=False)
        if self.session:
            self.authenticated = True
            update_token_expiration()

    def _set_status(self):
        """
        Setting Status From Status Code
        :return:
        """
        if str(self.status_code).startswith('2'):
            self.status = 'success'
        elif str(self.status_code).startswith('1') or str(self.status_code).startswith('3'):
            self.status = 'warning'
        elif str(self.status_code).startswith('4') or str(self.status_code).startswith('5'):
            self.status = 'danger'
        else:
            self.status = 'primary'
