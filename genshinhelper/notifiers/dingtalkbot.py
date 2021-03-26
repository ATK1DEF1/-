import base64
import hashlib
import hmac
import time
from urllib import parse

from genshinhelper import config
from .basenotifier import BaseNotifier


class DingTalkBot(BaseNotifier):
    def __init__(self):
        self.name = 'DingTalk Bot'
        self.token = config.DD_BOT_TOKEN
        self.retcode_key = 'errcode'
        self.retcode_value = 0

    def send(self, text='Genshin Impact Helper', status='status', desp='desp'):
        url = ''
        if config.DD_BOT_TOKEN:
            url = f'https://oapi.dingtalk.com/robot/send?access_token={config.DD_BOT_TOKEN}'
            if config.DD_BOT_SECRET:
                secret = config.DD_BOT_SECRET
                timestamp = int(round(time.time() * 1000))
                secret_enc = bytes(secret).encode('utf-8')
                string_to_sign = f'{timestamp}\n{secret}'
                string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
                hmac_code = hmac.new(
                    secret_enc, string_to_sign_enc,
                    digestmod=hashlib.sha256).digest()
                sign = parse.quote_plus(base64.b64encode(hmac_code))
                url = f'https://oapi.dingtalk.com/robot/send?access_token={config.DD_BOT_TOKEN}&timestamp={timestamp}&sign={sign}'

        data = {
            'msgtype': 'text',
            'text': {
                'content': f'{text} {status}\n\n{desp}'
            }
        }
        return self.push('post', url, data=data)
