# from .models import UserManager, Channel, ClientManager
# from .websocket import Websocketio
# from flask import request, json

# socketio = Websocketio.getInstances()
# user_manager = UserManager()
# client_manager = ClientManager()
#
#
# @socketio.on_error(namespace=socketio.name_space)
# def on_error(info):
#     print(f" # 错误异常, {info}")
#
#
# @socketio.on('connect', namespace=socketio.name_space)  # 有客户端连接会触发该函数
# def on_connect():  # 建立连接 sid:连接对象ID
#     sid = request.sid
#     client_manager.add_client(sid)
#     print(f' + 新建连接, cid={sid} count={client_manager.length}')
#
#
# @socketio.on('disconnect', namespace=socketio.name_space)  # 有客户端断开WebSocket会触发该函数
# def on_disconnect():  # 连接对象关闭 删除对象ID
#     sid = request.sid
#     client_manager.del_client(sid)
#     print(f" - 连接断开, cid={sid} count={client_manager.length}")
#
#
# @socketio.on('message', namespace=socketio.name_space)
# def on_message(message):
#     recv_items = json.loads(message)
#
#     userid = recv_items.get("userid")
#     message = recv_items.get("message")
#
#     client = user_manager.select_user(userid)
#     message_items = {
#         "client": client.to_dict(),
#         "message": message
#     }
#     print(f' # 收到消息, idcode={client.userid} message={message}')
#     socketio.send_message_by_channel(Channel.channel, message_items)
#
#
# @socketio.on('init', namespace=socketio.name_space)
# def on_init(message):
#     init_items = json.loads(message)
#     userid = init_items.get("userid", "")
#
#     client = user_manager.select_user(userid)
#
#     if len(userid) == 0 or client is None:
#         client = user_manager.create_user()
#         print(f' # 创建用户, idcode={client.userid}')
#
#     client.set_client_id(request.sid)
#     message_items = {"client": client.to_dict(), "message": message}
#
#     socketio.send_message_by_user(Channel.users, client.clientId, message_items)
#

# __all__ = ["socketio"]
