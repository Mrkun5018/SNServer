from server import startup_service, startup_websocket_service
from configer import mapping_config_object, SERVER
from utils.dbpool import initialize_database_pool
from blueprint import create_app_service


def create_app():
    mapping_config_object('server.ini')
    initialize_database_pool()
    server = create_app_service()
    return server


if __name__ == '__main__':
    application = create_app()
    print(" - -----------------------------------------------------")
    print(f" - SERVER RUN IN {SERVER.ENVIRONMENT.upper()} ENVIRONMENT")
    print(f" - SERVER VERSION {SERVER.VERSION}")
    print(" - -----------------------------------------------------")
    if SERVER.ENVIRONMENT == "development":
        startup_websocket_service(application)

    if SERVER.ENVIRONMENT == "production":
        startup_service(application)
