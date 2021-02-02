import logging
from http import HTTPStatus

from flask import Flask, session
from flask.json import jsonify
from flask_cors import CORS

from config.default import SECRET_KEY


def create_app(env: str = "dev"):
    """
    Create Sanic application with environment configuration

    :param env: Environment name to load the right config file

    :rtype flask.Flask:
    """
    app = Flask("flask-api")

    app.config.from_pyfile("./config/{}.py".format(env))

    cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*"}})
    # app.register_error_handler(404, not_found)

    return app
