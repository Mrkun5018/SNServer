# import eventlet
from flask import Flask
from flask_socketio import SocketIO
from utils.singleton import Singleton


class Websocketio(Singleton, SocketIO):

    def __init__(self, application: Flask, namespace="/websocket"):
        # eventlet.monkey_patch()
        super().__init__()
        self.name_space = namespace
        self.init_app(
            app=application,
            async_mode="threading",
            cors_allowed_origins='*'
        )

