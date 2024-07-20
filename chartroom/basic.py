from flask_socketio import Namespace, emit
from flask import request
import json


class Basic(object):
    def to_dict(self):
        """vars()"""
        attr_items = {}
        attributes = filter(lambda item: not item.startswith("__") and not item.endswith("__"), dir(self))
        for attr in attributes:
            attr_value = getattr(self, attr)
            if hasattr(attr_value, '__call__'):
                continue
            attr_items[attr] = attr_value
        return attr_items


class NamespaceHandler(Namespace):

    def __init__(self, namespace):
        super().__init__(namespace)
        self.__client_count = 0
        self.__error_count = 0

    def on_error(self, respond):
        self.__error_count += 1
        print(f" # 错误异常[{self.__client_count}], {respond}")

    def on_connect(self):
        sid = request.sid
        self.__client_count += 1
        print(f' + 新建连接, cid={sid} count={self.__client_count}')

    def on_disconnect(self):
        sid = request.sid
        self.__client_count -= 1
        print(f" - 连接断开, cid={sid} count={self.__client_count}")

    def send_message_to_channel(self, event, data, room):
        """指定一个客户端发送消息"""
        print(f" * 转发频道消息 {data}")
        self.emit(event=event, data=data)

    def send_message_to_user(self, event, client_id, reply_data):
        """对name_space下的所有客户端发送消息"""
        print(f" * 发送指定消息 {reply_data}")
        reply_item_chat = json.dumps(reply_data)
        emit(event, reply_item_chat, broadcast=False, namespace=self.namespace, to=client_id)

    def close_room(self, room, namespace=None):
        return super().close_room(room, namespace)

    def query_rooms(self, sid=None):
        return self.rooms(sid=sid)

    def enter_room(self, sid, room, namespace=None):
        return super().enter_room(sid, room)

    def leave_room(self, sid, room, namespace=None):
        return super().leave_room(sid, room, namespace=namespace)
