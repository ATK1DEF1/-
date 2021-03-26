import json

from genshinhelper import config
from .basenotifier import BaseNotifier


class CustomNotifier(BaseNotifier):
    def __init__(self):
        self.name = 'Custom Notifier'
        self.conf = json.loads(config.CUSTOM_NOTIFIER)
        self.url = self.conf['url']
        self.data = self.conf['data']
        self.token = self.conf['data']
        self.retcode_key = self.conf['retcode_key']
        self.retcode_value = self.conf['retcode_value']

    def send(self, text='Genshin Impact Helper', status='status', desp='desp'):
        if not self.token:
            return self.push('post', '')

        title = f'{text} {status}'
        if self.conf['merge_title_and_desp']:
            title = f'{text} {status}\n\n{desp}'

        if self.conf['set_data_title'] and self.conf['set_data_sub_title']:
            self.conf['data'][self.conf['set_data_title']] = {
                self.conf['set_data_sub_title']: title
            }

        elif self.conf['set_data_title'] and self.conf['set_data_desp']:
            self.conf['data'][self.conf['set_data_title']] = title
            self.conf['data'][self.conf['set_data_desp']] = desp

        elif self.conf['set_data_title']:
            self.conf['data'][self.conf['set_data_title']] = title

        if self.conf['method'].upper() == 'GET':
            return self.push('get', self.url, params=self.data)
        elif self.conf['method'].upper() == 'POST' and self.conf['data_type'].lower(
        ) == 'json':
            return self.push('post', self.url, json=self.data)
        else:
            return self.push('post', self.url, data=self.data)
