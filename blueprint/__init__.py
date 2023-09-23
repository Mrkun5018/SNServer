from utils import Logger
import importlib
import os


def auto_register_blueprint(application, b_file_name=None, ignore=None):  # 蓝图注册
    log = Logger.getInstances()

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

        log.warning(f"- auto register blueprint -> {filename}")
        auto_blueprint = importlib.import_module(f'{b_file_name}.' + filename).__dict__[filename]
        application.register_blueprint(auto_blueprint)


__all__ = ["auto_register_blueprint"]


