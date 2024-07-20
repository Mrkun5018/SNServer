class SERVER:
    VERSION = 'SUPER NOTES SERVER v1.0.1'
    PORT = 8080
    HOST = '127.0.0.1'
    DEBUG = True
    ENVIRONMENT = "production"        # production or development


class LOCAL:
    FILEPATH = './source/upload'
    IMAGE = 'image'
    AVATAR = 'avatar'
    PICTURES = 'pictures'


class MYSQL:
    PORT = 3306
    HOST = '127.0.0.1'
    USERNAME = 'root'
    PASSWORD = 'root'
    DATABASE = 'notes'


class JWT:
    KEY = None
