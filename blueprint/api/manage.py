from flask import request, Response

from utils import respond_handle_wrapper
from utils.manager import getCurrentTimeStr, attr_local_image
from configer import SERVER, LOCAL

from blueprint.api import api
from lxml import etree
import requests
import os

uat = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def request_handle(_url):
    headers = {"user-agent": uat}
    return requests.get(_url, headers=headers)


@api.route('/spider', methods=['GET'])
@respond_handle_wrapper
def applets_spider():
    link = request.args.get('link')
    linklist = []
    if link is not None:
        respond = request_handle(link)
        if respond.status_code == 200:
            choose = '//*[contains(@class,"RichText ztext CopyrightRichText-richText")]'
            xpath_obj = etree.HTML(respond.text).xpath(choose)[0]
            linklist = xpath_obj.xpath('./figure/img/@data-original')
    return linklist


@api.route('/upload/image', methods=['POST'])
@respond_handle_wrapper
def upload_image():
    upload_file = request.files.get('note-image')
    uploadName = upload_file.filename
    suffix = os.path.splitext(uploadName)[1]
    filename = f"{getCurrentTimeStr()}{suffix}"
    filepath = os.path.join(LOCAL.FILEPATH, LOCAL.IMAGE, filename)
    upload_file.save(filepath)
    return {'url': f"image/{filename}"}


@api.route("<string:typeof>/<string:name>")
@respond_handle_wrapper
def query_image(typeof, name):
    typeof_map = {'image': LOCAL.IMAGE, 'avatar': LOCAL.AVATAR, 'pictures': LOCAL.PICTURES}
    image_path = typeof_map.get(typeof, None)
    if image_path is not None:
        filebytes = attr_local_image(os.path.join(LOCAL.FILEPATH, image_path), name)
        return Response(filebytes, mimetype='image/jpeg')
    return None


@api.route('/query/avatar/<string:username>')
@respond_handle_wrapper
def query_avatar(username):     # 获取头像
    avatar_map = {'admin': '1667401317650.jpeg'}
    avatar_name = avatar_map.get(username, None)
    return {'link': f"avatar/{avatar_name}"} if avatar_name else None


@api.route('/upload/avatar')
@respond_handle_wrapper
def upload_avatar():     # 上传头像
    username = request.args.get('user')
    pass

