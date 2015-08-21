from functools import wraps
from flask import request
from app.config_handler import users

def check_request(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        checker = request.args.get('checker', False)
        if checker:
            user = checker.decode('base64')
            if user in users:
                return func(*args, **kwargs)
            else:
                return ""
        else:
            return ""

    return decorated_function
