from genshinhelper import config

from .basenotifier import BaseNotifier


class ServerChanTurbo(BaseNotifier):
    def __init__(self):
        self.name = 'Server Chan Turbo'
        self.token = config.SCTKEY
        self.retcode_key = 'errno'
        self.retcode_value = 0

    def send(self, text, status, desp):
        url = f'https://sct.ftqq.com/{SCKEY}.send'
        data = {
            'text': f'{text} {status}', 
            'desp': desp
        }
        return self.push('post', url, data=data)
