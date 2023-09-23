from flask import g, request
from utils import SALT
from jwt import exceptions
import jwt
import functools
import datetime

# 构造header
headers = {'typ': 'jwt', 'alg': 'HS256'}


def createToken(username, password):
    # 构造payload
    payload = {
        'username': username,
        'password': password,  # 自定义用户ID
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
    }
    return jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)


def loginRequired(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if g.username == 1:
                return {'code': 4001, 'message': 'token已失效'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': 'token认证失败'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': '非法的token'}, 401
            else:
                return f(*args, **kwargs)
        except BaseException as e:
            print(e)
            return {'code': 4001, 'message': '请先登录认证.'}, 401
    return wrapper


def jwt_authentication():
    # 1.获取请求头Authorization中的token
    # 2.判断是否以 Bearer开头
    # 3.使用jwt模块进行校验
    # 4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存

    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):  # "校验token"
        g.username = None
        try:
            "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符, 判断token的校验结果"
            payload = jwt.decode(auth[7:], SALT, algorithms=['HS256'])
            g.username = payload.get('username')       # 获取载荷中的信息赋值给g对象
        except exceptions.ExpiredSignatureError:  # 'token已失效'
            g.username = 1
        except jwt.DecodeError:  # 'token认证失败'
            g.username = 2
        except jwt.InvalidTokenError:  # '非法的token'
            g.username = 3
