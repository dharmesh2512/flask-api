import os

from flask import jsonify

# from apis import app
from applications import create_app
from config.default import PORT

# from routes import api_routes
from routes import initializer_api
from utils.exception_handler import FlaskGenericException

app_env = os.environ.get("FLASK_ENV", "dev")

app = create_app(app_env)


@app.errorhandler(FlaskGenericException)
def handle_flask_generic_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


api_routes = initializer_api()

app.register_blueprint(api_routes)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", PORT))
    app.run(debug=True)
