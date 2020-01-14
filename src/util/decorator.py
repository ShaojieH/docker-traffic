from functools import wraps

from util.web import wrap_response


def api_response(func):
    @wraps(func)
    def create_json_response(*args, **kwargs):
        response = func(*args, **kwargs)
        return wrap_response(response)

    return create_json_response
