from urllib import parse
from genshinhelper import config

from .basenotifier import BaseNotifier


class Bark(BaseNotifier):
    def __init__(self):
        self.name = 'Bark App'
        self.token = config.BARK_KEY
        self.retcode_key = 'code'
        self.retcode_value = 200

    def send(self, text, status, desp):
        url = f'{config.BARK_KEY}/{text} {status}/{parse.quote(desp)}'
        data = {'sound': config.BARK_SOUND}
        return self.push('get', url, params=data)

