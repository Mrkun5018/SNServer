from utils.manager import IDGenerator
from faker import Faker

from .basic import Basic, NamespaceHandler
from .user import User


class Channel(Basic):

    def __init__(self, idcode: str, founder: str, title: str, avatar: str, description: str):
        self.id = idcode
        self.title = title
        self.avatar = avatar
        self.description = description
        self.founder = founder

        self.users: list[str] = []

    def is_founder(self, userid) -> bool:
        return self.founder == userid

    def add_user(self, userid) -> bool:
        if userid in self.users:
            return True
        self.users.append(userid)
        return True

    def del_user(self, userid) -> bool:
        if userid not in self.users:
            return False
        self.users.remove(userid)
        return True

    def has_user(self, userid) -> bool:
        return userid in self.users


class ChannelManager(object):
    def __init__(self, server: NamespaceHandler):
        self.__server = server
        self.namespace = server.namespace
        self.idGenerator = IDGenerator()
        self.fake = Faker()
        self.channel_tables: dict[str, Channel] = {}

    def create_channel(self, founder: User, name, description, idcode=None) -> Channel:
        params = ','.join([founder.userid, founder.clientId])
        idcode = idcode or self.idGenerator.generate(params)

        avatar = 'https://img1.imgtp.com/2023/10/16/GwTmOB8r.jpeg'
        channel = Channel(
            idcode=idcode,
            title=name,
            avatar=avatar,
            description=description,
            founder=founder.userid
        )
        channel.add_user(founder.userid)
        self.channel_tables[idcode] = channel
        if founder.userid != 'builder':
            self.__server.enter_room(sid=founder.clientId, room=name)
        return channel

    def query_channels(self):
        return list(self.channel_tables.values())

    def query_rooms(self, sid=None):
        if sid is None:
            return list(self.channel_tables.keys())
        return self.__server.query_rooms(sid)

    def enter_room(self, sid, name):
        if name not in self.channel_tables.keys():
            return False
        self.__server.enter_room(sid=sid, room=name)
        return self.channel_tables[name].add_user(sid)

    def leave_room(self, sid, name):
        if name not in self.channel_tables.keys():
            return False
        self.channel_tables[name].del_user(sid)
        self.__server.leave_room(sid=sid, room=name)
        return True

    def close_room(self, founder: User, name):
        channel = self.channel_tables.get(name, None)
        if channel is None:
            return False
        if not channel.is_founder(founder.userid):
            return False

        self.__server.close_room(name)
        return True
