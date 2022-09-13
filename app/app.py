import json

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restx import Api
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from app.constants import app_constants


def init_app():
    """Spawns the application"""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CORS(app)

    # Set Flask configuration
    app.config['ERROR_404_HELP'] = False

    # Register application endpoints using Blueprint
    blueprint = Blueprint("api", __name__, url_prefix=f'/{app_constants["api_version"]}')
    api = Api(blueprint,
              title=app_constants["service_name"],
              version=app_constants["api_version"],
              description=app_constants["service_description"],
              doc='/docs/')

    register_namespaces(api)
    app.register_blueprint(blueprint)

    # Register error handlers
    @app.errorhandler(HTTPException)
    def app_error_handler(err):
        response = err.get_response()
        response.data = json.dumps({
            "code": err.code,
            "name": err.name,
            "message": err.description,
        })
        response.content_type = "application/json"
        return response

    @api.errorhandler(HTTPException)
    def api_error_handler(err):
        data = {
            "code": err.code,
            "name": err.name,
        }
        return data, err.code

    return app


def register_namespaces(app_api):
    """Adds the namespaces to the application"""
    from app.api.example.controller import ns as example_namespace
    app_api.add_namespace(example_namespace, path='/api/example')

    # Add more namespaces here

