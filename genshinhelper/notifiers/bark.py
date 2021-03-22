from urllib import parse
from .basenotifier import BaseNotifier
from genshinhelper import config


class Bark(BaseNotifier):
    def send(self, text, status, desp):

        url = f'{config.BARK_KEY}/{text} {status}/{parse.quote(desp)}'
        data = {'sound': config.BARK_SOUND}
        name, token, retcode_key, retcode_value = [
            'Bark App', config.BARK_KEY, 'code', 200
        ]
        return self.push(
            'get',
            url,
            params=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)
