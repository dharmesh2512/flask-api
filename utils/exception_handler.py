from flask import Blueprint, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES


class FlaskGenericException(Exception):
    status_code = 500  # default unless overridden

    def __init__(self, message, status_code=None, payload=None, error_message=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.error_message = error_message

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["status_code"] = self.status_code
        rv["message"] = self.message
        rv["errors"] = self.error_message
        return rv


class ValidationError(FlaskGenericException):
    status_code = 400
