from flask import Response, jsonify
import traceback
import functools


class RespondHandle(object):
    """
    100
    200=> OK 请求成功。一般用于GET与POST请求
    300
    401=> Bad Request 客户端请求的语法错误, 服务器无法理解
    500
    """
    def __init__(self):
        self.reason = {
            "message": "",
            "code": 200
        }
        self.data = []
        self.status_code = 200
        self.fileObject = None

    def setStatus(self, status: int):
        self.status_code = status
        self.reason['code'] = status

    def setMessage(self, msg: str):
        self.reason["message"] = msg

    def setContent(self, data):
        self.data = data

    def setFileObject(self, file):
        self.fileObject = file

    def getRespond(self):
        if self.fileObject:
            return self.fileObject, 200
        return jsonify({"reason": self.reason, "data": self.data}), 200


def respond_handle_wrapper(function):
    @functools.wraps(function)
    def function_wrapper(*args, **kwargs):
        respond_handle = RespondHandle()
        try:
            respond = function(*args, **kwargs)

            if respond is None:
                return

            if isinstance(respond, Response):
                respond_handle.setFileObject(respond)
                return

            respond_handle.setContent(respond)

        except Exception as err:
            respond_handle.setMessage(f"server error: {repr(err)}")
            respond_handle.setStatus(500)
        finally:
            return respond_handle.getRespond()

    return function_wrapper



