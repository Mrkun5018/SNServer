from application import create_application
from configer import mapping_config_object, SERVER
from utils.dbpool import initialize_database_pool


def create_app():
    mapping_config_object('server.ini')
    initialize_database_pool()
    application = create_application()
    application.logger.info(f" - RUN IN PRODUCTION {SERVER.VERSION}")
    return application


