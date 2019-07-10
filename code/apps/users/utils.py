import hashlib
import json
from time import time

import requests


def send_sms(mobile):
    url = 'https://api.netease.im/sms/sendcode.action'
    data = {'mobile': mobile}
    # 4部分组成 headers： AppKey  Nonce  CurTime  CheckSum
    AppKey = '1bdcdeda105c1d91e802a191d8f5ed94'
    Nonce = '843hjfd87fdfshdjfhs5433'
    CurTime = str(time())
    AppSecret = '05bf2ece7293'
    content = AppSecret + Nonce + CurTime
    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()

    headers = {'AppKey': AppKey, 'Nonce': Nonce, 'CurTime': CurTime, 'CheckSum': CheckSum}

    response = requests.post(url, data, headers=headers)
    # json
    str_result = response.text  # 获取响应体

    json_result = json.loads(str_result)  # 转成json

    return json_result