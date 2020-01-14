from flask import jsonify


def wrap_response(response):
    return jsonify(response)
