import os
import re
import json
import uuid
import time
from datetime import datetime


class SourceHandle(object):
    NotesDict = {}


class IDGenerator(object):

    def __init__(self, *args):
        self.hashset = set(args)
        self.fields = ('author', 'content')

    def checkHashcode(self, code):
        return code not in self.hashset

    @staticmethod
    def __generate_idcode(params=None):
        params = list(params) or []
        params.append(str(time.time()))
        uid = uuid.uuid3(uuid.NAMESPACE_DNS, ','.join(params))
        return str(uid).replace('-', '')

    def generate(self, *args):
        while idcode := IDGenerator.__generate_idcode(args):
            if self.checkHashcode(idcode):
                self.hashset.add(idcode)
                return idcode


def getCurrentTimeStr(fmt: str = None) -> str:
    return datetime.now().strftime(fmt or '%Y%m%d%H%M%S')


def saveJsonFile(data: dict, filepath: str, filename: str, mode="w+"):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(os.path.join(filepath, filename), mode, encoding="utf-8") as file:
        json.dump(data, fp=file, ensure_ascii=False)


def loadJsonFile(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def remove_special_characters(char: str) -> [str]:
    split_result = []
    if len(char) > 0:
        pattern = '[’!"\\#$%&\'()＃！，。/（）*+,:;<=>?\\@：?￥★、…＞【】［］『』《》？「」“”‘’\\[\\]^`{|}~\\u4e00 \\u9fa5]+'
        remove_result = re.sub(pattern, ' ', char)
        split_result: [str] = ' '.join(remove_result.split()).split(' ')
    return split_result


def timestampFormatString(timestamp: float or int) -> str:
    _time_arr = time.localtime(timestamp)
    _time_str = time.strftime("%Y-%m-%d %H:%M:%S", _time_arr)
    return _time_str


def datetimeFormatString(dt: datetime, fmt: str = None) -> str:
    if not isinstance(dt, datetime):
        return ""
    DSMap = {"date": ["%Y", "%m", "%d"], "time": ["%H", "%M", "%S"]}
    DSFmt = {"date": "-", "time": ":", "default": " "}
    if fmt in DSMap:
        _fmt = DSFmt[fmt].join(DSMap[fmt])
    else:
        _date = DSFmt["date"].join(DSMap["date"])
        _time = DSFmt["time"].join(DSMap["time"])
        _fmt = DSFmt["default"].join([_date, _time])
    return dt.strftime(_fmt)


def attr_local_image(path, name):
    assert name in os.listdir(path)
    image_path = os.path.join(path, name)
    with open(image_path, 'rb') as file:
        return file.read()
