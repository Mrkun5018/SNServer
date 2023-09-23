from configer.parser import mapping_config_object
from utils import Logger, DatabaseConnectionPool, jwt_authentication
from blueprint import auto_register_blueprint
from configer import Configer, SERVER, MYSQL
from flask_cors import CORS
from flask import Flask

application = Flask(__name__)
Logger(application)
CORS(application)

mapping_config_object('app_server.ini')

DatabaseConnectionPool(
    user=MYSQL.USERNAME,
    password=MYSQL.PASSWORD,
    dbname=MYSQL.DATABASE,
    host=MYSQL.HOST,
    port=MYSQL.PORT
)

auto_register_blueprint(application=application, b_file_name='blueprint', ignore=['admin'])


@application.route('/')
def index():
    return "<h1 align='center'>super　notes　server</h1>"


if __name__ == '__main__':
    application.config.from_object(Configer)  # 引入配置类
    application.before_request(jwt_authentication)
    application.run(debug=SERVER.DEBUG, port=SERVER.PORT)
