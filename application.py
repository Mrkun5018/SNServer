from blueprint import server_blueprints
from utils import jwt_authentication
from configer import Configer
from flask import Flask
import flask_cors


def create_application() -> Flask:
    application = Flask(__name__, static_folder='./source', static_url_path='/source')

    flask_cors.CORS(application)

    for filename, blueprint in server_blueprints(b_file_name='blueprint', ignore=['admin']):
        print(f" * register blueprint => {filename}")
        application.register_blueprint(blueprint)

    application.config.from_object(Configer)

    application.before_request(jwt_authentication)

    return application


__all__ = ["create_application"]
