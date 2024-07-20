from chartroom.namespace import ChatroomHandler
from chartroom.websocket import Websocketio
from configer import SERVER
from flask import Flask


def startup_service(application: Flask):
    from gevent import pywsgi, monkey
    monkey.patch_all()
    pywsgi.WSGIServer(
        (SERVER.HOST, SERVER.PORT),
        application
    ).serve_forever()


def startup_websocket_service(application: Flask):
    socketio = Websocketio(application)
    chatroom = ChatroomHandler(socketio.name_space)
    socketio.on_namespace(chatroom)
    socketio.run(
        app=application,
        port=SERVER.PORT,
        host=SERVER.HOST,
        debug=SERVER.DEBUG,
        allow_unsafe_werkzeug=True
    )


__all__ = ["startup_websocket_service", "startup_service"]
