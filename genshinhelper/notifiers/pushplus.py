from genshinhelper import config

from .basenotifier import BaseNotifier


class PushPlus(BaseNotifier):
    def __init__(self):
        self.name = 'pushplus'
        self.token = config.PUSH_PLUS_TOKEN
        self.retcode_key = 'code'
        self.retcode_value = 200

    def send(self, text='Genshin Impact Helper', status='status', desp='desp'):
        url = 'https://pushplus.hxtrip.com/send'
        data = {
            'token': config.PUSH_PLUS_TOKEN,
            'title': f'{text} {status}',
            'content': desp,
            'topic': config.PUSH_PLUS_USER
        }
        return self.push('post', url, data=data)
