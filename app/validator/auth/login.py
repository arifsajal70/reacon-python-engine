# Import Flask Things
from flask import request

# Import Helpers
from app.helpers.response import Response

# Import Utils
from functools import wraps


def validate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        """Reset Error In Every Request"""
        form_data = request.values
        errors = {}

        """Username Validation"""
        if 'username' in form_data and len(form_data.get('username')) > 0:
            if not isinstance(form_data.get('username'), str):
                errors.update({'username': 'Username Should Be String.'})
        else:
            errors.update({'username': 'Username Field Is Required.'})

        """Message Validation"""
        if 'password' in form_data and len(form_data.get('password')) > 0:
            if not isinstance(form_data.get('password'), str):
                errors.update({'password': 'Password Should Be Alpha Numeric.'})
        else:
            errors.update({'password': 'Password Field is required.'})

        """Return error if error exists, Otherwise move forward"""
        return len(errors) > 0 and Response(errors=errors, status_code=406, message='Invalid Information Submitted.')\
            .send() or function(*args, **kwargs)

    return wrapper
