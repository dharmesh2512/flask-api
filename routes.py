from flask import Blueprint
from flask_restful import Api as _Api
from flask_restful import HTTPException

from apis.payment.views import ProcessPaymentAPI


class Api(_Api):
    def error_router(self, original_handler, e):
        # Override original error_router to only handle HTTPExceptions.
        if self._has_fr_route() and isinstance(e, HTTPException):
            try:
                # Use Flask-RESTful's error handling method
                return self.handle_error(e)
            except Exception:
                # Fall through to original handler (i.e. Flask)
                pass
        return original_handler(e)


def initializer_api():

    api_routes = Blueprint("external", __name__, url_prefix="/api")

    # api = Api(api_routes, errors=errors)
    api = Api(api_routes)

    # Payment Process
    api.add_resource(ProcessPaymentAPI, "/process/payment", methods=["POST"])

    return api_routes
