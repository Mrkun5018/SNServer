from configer import SERVER
from application import create_application
from configer import mapping_config_object
from utils.dbpool import initialize_database_pool


if __name__ == '__main__':
    mapping_config_object('server.ini')
    initialize_database_pool()
    application = create_application()
    application.logger.debug(f" - RUN IN DEVELOPMENT {SERVER.VERSION}")
    application.run(debug=SERVER.DEBUG, port=SERVER.PORT, host=SERVER.HOST)
