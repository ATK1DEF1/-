from .basenotifier import BaseNotifier


class WwBot(BaseNotifier):
    def notify(self, text, status, desp):
        from config import WW_BOT_KEY

        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WW_BOT_KEY}'
        data = {
            'msgtype': 'text',
            'text': {
                'content': f'{text} {status}\n\n{desp}'
            }
        }
        name, token, retcode_key, retcode_value = [
            '企业微信机器人', WW_BOT_KEY, 'errcode', 0
        ]
        return self.push(
            'post',
            url,
            json=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

