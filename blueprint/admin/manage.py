from utils import datetimeFormatString, respond_handle_wrapper
from configer import SERVER
from utils.constant import USERS, ADMIN
from utils.verify import createToken
from blueprint.admin import admin
from flask import request
from datetime import datetime
import random
import os
import re


@admin.route('/')
@respond_handle_wrapper
def main():
    return "admin main"


@admin.route('/<string:typeof>/login', methods=['GET', 'POST'])  #
def login(typeof):
    data = request.json
    if typeof == ADMIN:
        username = data.get("username")
        password = data.get("password")
        # 验证账号密码，正确则返回token，用于后续接口权限验证
        if username == "admin" and password == "123456":
            token = createToken(username, password)
            userinfo = {'username': 'admin', 'avatar': '1667401317650.jpeg'}
            return {"code": 200, "message": "登录成功", "data": userinfo, "token": token}
        else:
            return {"code": 501, "message": "账号或密码不正确"}
    elif typeof == USERS:
        print("普通用户申请登录")
    else:
        return {"code": 201, "message": "type is false"}


@admin.route('/menu')
@respond_handle_wrapper
def query_menu():
    return [
        {"index": 0, "path": '/admin/home', "desc": '首页'},
        {"index": 1, "path": '/admin/notes', "desc": '笔记'},
        {"index": 2, "path": '/admin/album', "desc": '图库'},
        {"index": 3, "path": '/admin/applets', "desc": '程序'},
        {"index": 4, "path": '/admin/collection', "desc": '藏品'},
    ]


@admin.route('/update', methods=["POST"])
@respond_handle_wrapper
def update_notes():
    params = request.json or request.form.to_dict()
    md5 = params.pop("md5", None)
    # query_field = ('tags', 'content', 'title', 'status', 'useful')
    # query_res: dict = Library.query.filter(Library.md5 == md5).first().to_dict()
    # screen_items = filter(lambda item: item[0] in query_field and item[1] is not None, params.items())
    # screen_dict = {key: val for key, val in screen_items}
    # query_res.update(screen_dict)
    # Library.query.filter(Library.md5 == md5).update(query_res)
    # db.session.commit()


@admin.route('/append', methods=["POST", "PUT"])
@respond_handle_wrapper
def append_notes():  # author, title, tags, content 
    params = request.json or request.form.to_dict()
    # return dbHandler.insert(params)


@admin.route('/upload/notes', methods=['POST'])
@respond_handle_wrapper
def upload_notes():
    file = request.files.get('file')
    if file.mimetype in ('image/jpeg',):
        return None
    form = request.form.to_dict()
    create_time = form.pop('createTime')
    content = file.stream.read().decode('utf-8')
    create_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    form.update({'content': content, 'timestamp': create_time})
    # dbHandler.insert(form)
    return True


@admin.route('/delete', methods=["DELETE"])
@respond_handle_wrapper
def delete_notes():
    args = request.args.to_dict()
    user, code = args.get('user', None), args.get('code', None)
    if code is None or user is None:
        return "Missing parameter"

    # note = dbHandler.delete(md5=code, author=user)
    # match_images = re.findall(r"/image/(.*\d\.png)]", note.content)
    # image_site = os.path.join(os.getcwd(), 'source', 'upload', 'image')
    # image_array = os.listdir(image_site)
    # for image in match_images:
    #     if image in image_array:
    #         remove_path = os.path.join(image_site, image)
    #         os.remove(remove_path)


@admin.route('/queryNoteList', methods=['GET'])
@respond_handle_wrapper
def query_note_list():
    params = request.args.to_dict()
    page = int(params.pop("page"))
    num = int(params.pop("num"))
    # count = Library.query.count()
    # alldata = Library.query.filter_by(**params).paginate(page=page, per_page=num)
    # note_list = modelHandler.toList(alldata.items)
    # for index, note in enumerate(note_list):
    #     note["timestamp"] = datetimeFormatString(note["timestamp"], "date")
    #     tags = note['tags']
    #     note['tags'] = [] if tags is None else tags.split(',')
    #     note['visible'] = False
    #     note["id"] = index + 1
    # return {"total": count, "notes": note_list}


@admin.route('/queryNote', methods=['GET'])
@respond_handle_wrapper
def query_note():
    params = request.args.to_dict()
    author = params.get('author', None)
    # md5 = params.get('md5', None)
    # if md5 and author:
    #     alldata = Library.query.filter_by(author=author, md5=md5).first()
    #     data = modelHandler.toDict(alldata)
    #     time = data["timestamp"]
    #     tags = data['tags']
    #     data['tags'] = tags.split(',')
    #     data["createTime"] = datetimeFormatString(time, "date")
    #     return data


@admin.route('queryRandomPictures', methods=['GET'])
@respond_handle_wrapper
def query_random_pictures():
    filenames = os.listdir(os.path.join(SERVER.FILEPATH, SERVER.PICTURES))
    fileSize = len(filenames)
    if fileSize == 0:
        return "not found pictures"
    pictures_name = filenames[random.randint(0, fileSize - 1)]
    return {'link': f"pictures/{pictures_name}"}
