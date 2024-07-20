from flask import request, json

from .user import UserManager
from .channel import ChannelManager
from .basic import NamespaceHandler

USERS = 'users'
PUBLIC_CHANNELS = 'public_channels'
INVOLUTION_PLUS_CHANNELS = 'involution_plus_channels'
""" 
- channel           
- channel_message   => 用于接收 所有频道的数据, 按照所在的room转发
- channel_create    => 
- channel_delete    =>
- channel_notice    => 广播有消息的频道, 消息体: channelId[频道标识], message_count[消息数量], message_index[消息索引]
"""
CHANNELS = 'channels'
CHANNEL_MESSAGE = 'channel_message'
CHANNEL_CREATE = 'channel_create'
CHANNEL_DELETE = 'channel_delete'
CHANNEL_NOTICE = 'channel_notice'

"""
room
PUBLIC_CHANNELS  大厅
"""


class ChatroomHandler(NamespaceHandler):

    def __init__(self, namespace='chatroom'):
        super().__init__(namespace)
        self.user_manager = UserManager()
        self.channel_manager = ChannelManager(self)

        builder = self.user_manager.create_user()

        self.channel_manager.create_channel(
            builder,
            name="大厅",
            description="Hi, 来自五湖自嗨的8U",
            idcode=PUBLIC_CHANNELS
        )

        self.channel_manager.create_channel(
            builder,
            name="内卷风云Plus",
            description="内卷打卡，分享内卷知识经验",
            idcode=INVOLUTION_PLUS_CHANNELS
        )

    def on_connect(self):
        super().on_connect()
        sid = request.sid
        self.channel_manager.enter_room(sid, PUBLIC_CHANNELS)
        # 发送所有的频道信息 ################################################
        channels = self.channel_manager.query_channels()
        channel_items = list(map(lambda item: item.to_dict(), channels))
        self.send_message_to_user(CHANNELS, sid, channel_items)
        # 发送用户信息 #############################################################
        client = self.user_manager.create_user(client_id=sid)
        self.send_message_to_user(
            USERS, client.clientId, {
                "client": client.to_dict(),
                "message": 'The new user is created successfully'
            }
        )

    def on_users_init(self, respond):
        sid = request.sid
        init_items = json.loads(respond)
        userid = init_items.get("userid", None)
        if userid is None:
            client = self.user_manager.select_user(userid)
            client.set_client_id(sid)

    def on_channel_message(self, respond):
        """
        channels_message  => 用于接收 所有频道的数据, 按照所在的room转发
        :param respond: key => room、userid、message
        :return:
        """
        recv_data = json.loads(respond)
        message = recv_data["message"]
        userid = recv_data["userid"]
        channel = recv_data["channel"]
        print(f" * 接收频道消息 {recv_data}")
        client = self.user_manager.select_user(userid)
        message_items = {
            "client": client.to_dict(),
            "message": message,
            "channel": channel
        }
        print(" * rooms", self.query_rooms(client.clientId))
        self.send_message_to_channel(CHANNEL_MESSAGE, message_items, channel)
