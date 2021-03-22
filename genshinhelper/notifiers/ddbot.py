import time
import hmac
import hashlib
import base64
from urllib import parse
from .basenotifier import BaseNotifier


class DdBot(BaseNotifier):
    def notify(self, text, status, desp):
        from config import DD_BOT_TOKEN, DD_BOT_SECRET

        url = ''
        if DD_BOT_TOKEN:
            url = f'https://oapi.dingtalk.com/robot/send?access_token={DD_BOT_TOKEN}'
            if DD_BOT_SECRET:
                secret = DD_BOT_SECRET
                timestamp = int(round(time.time() * 1000))
                secret_enc = bytes(secret).encode('utf-8')
                string_to_sign = f'{timestamp}\n{secret}'
                string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
                hmac_code = hmac.new(
                    secret_enc, string_to_sign_enc,
                    digestmod=hashlib.sha256).digest()
                sign = parse.quote_plus(base64.b64encode(hmac_code))
                url = 'https://oapi.dingtalk.com/robot/send?access_' \
                    f'token={DD_BOT_TOKEN}&timestamp={timestamp}&sign={sign}'

        data = {
            'msgtype': 'text',
            'text': {
                'content': f'{text} {status}\n\n{desp}'
            }
        }
        name, token, retcode_key, retcode_value = [
            '钉钉机器人', DD_BOT_TOKEN, 'errcode', 0
        ]
        return self.push(
            'post',
            url,
            data=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

