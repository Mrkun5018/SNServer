from flask import Flask
import flask_cors
import importlib
import os

from utils import jwt_authentication
from configer import Configer


def auto_import_blueprints(b_file_name=None, ignore=None) -> []:  # 蓝图注册
    ignore = ignore or []
    ignore.append("__pycache__")

    b_file_name = b_file_name or 'blueprint'

    for filename in os.listdir(b_file_name):
        if filename in ignore:
            continue

        filepath = os.path.join(b_file_name, filename)
        if not os.path.isdir(filepath):
            continue

        if not os.path.exists(os.path.join(filepath, '__init__.py')):
            continue

        blueprint = importlib.import_module(f'{b_file_name}.' + filename).__dict__[filename]
        yield filename, blueprint


def create_app_service() -> Flask:
    application = Flask(__name__, static_folder='./source', static_url_path='/source')

    flask_cors.CORS(application)

    for filename, blueprint in auto_import_blueprints(b_file_name='blueprint', ignore=['admin']):
        print(f" * register blueprint => {filename}")
        application.register_blueprint(blueprint)

    application.config.from_object(Configer)

    application.before_request(jwt_authentication)

    application.add_url_rule('/', 'index', index)

    return application


def index():
    return "<h1 align='center'>super　notes　server</h1>"


__all__ = ["create_app_service"]


