from flask import logging
from configer import SERVER
from utils.singleton import Singleton


class Logger(Singleton):

    def __init__(self, app):
        self.logger = logging.create_logger(app)
        self.warning(msg=f"- CURRENT VERSION[{SERVER.VERSION}]")

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)


if __name__ == '__main__':
    # logger1 = Logger(1)
    # logger2 = Logger(2)
    logger3 = Logger.getInstances()
    # print(logger2 == logger1 == logger3)
