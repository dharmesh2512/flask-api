from flask import jsonify
from flask_restful import abort


def error_response(error_message=None, code=400, status=None):
    abort(code, code=code, status=status, error=error_message)


def success_response(message=None, code=200, status=None, data=None):
    return jsonify({"code": code, "status": status, "message": message, "data": data})
