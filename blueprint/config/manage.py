from blueprint.config import config
from utils import respond_handle_wrapper


@config.route('/menu', methods=['GET'])
@respond_handle_wrapper
def query_menu():
    return [
        {"label": "个人主页", "path": "/"},
        {"label": "随手笔记", "path": "/notes"},
        {"label": "实用工具", "path": "/applet"},
        {"label": "即时聊天", "path": "/chatroom"},
        {"label": "代码片段", "path": "/snippets"},
        # {"label": "关于", "path": "/about"}
    ]

