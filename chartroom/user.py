from .basic import Basic
from utils.manager import IDGenerator
from faker import Faker
import random


class User(Basic):
    BUILDER = 'builder'

    def __init__(self, client_id, userid="", nickname="", sex="", avatar="", addr=""):
        self.clientId = client_id
        self.userid = userid
        self.nickname = nickname
        self.avatar = avatar
        self.sex = sex
        self.addr = addr

    def set_client_id(self, cid):
        self.clientId = cid

    def is_builder(self):
        return self.clientId == User.BUILDER == self.userid


class UserManager(object):

    def __init__(self):
        self.idGenerator = IDGenerator()
        self.fake = Faker()
        self.client_tables: dict[str, User] = {}
        self.create_user()

    def get_builder(self):
        return self.client_tables.get(User.BUILDER)

    def create_user(self, client_id=User.BUILDER) -> User:
        if client_id == User.BUILDER:
            userid = User.BUILDER
        else:
            userid = self.idGenerator.generate(client_id)

        if userid in self.client_tables.keys():
            return self.client_tables[userid]

        sex = "male" if random.randint(0, 1) else "woman"

        user = User(
            client_id=client_id,
            userid=userid,
            nickname=self.fake.name(),
            sex=sex,
            addr=self.fake.address(),
            avatar='https://img1.imgtp.com/2023/10/16/GwTmOB8r.jpeg'
        )

        self.client_tables[userid] = user

        return user

    def remove_user(self, userid) -> 'User':
        client = self.client_tables.pop(userid)
        return client

    def select_user(self, userid) -> 'User':
        return self.client_tables.get(userid)

    def select_user_by_cid(self, cid):
        find_user = filter(lambda user: user.clientId == cid, self.client_tables.values())
        return find_user
