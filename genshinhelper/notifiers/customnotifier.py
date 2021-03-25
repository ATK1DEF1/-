from genshinhelper import config

from .basenotifier import BaseNotifier
from ..utils import log, to_python


class CustomNotifier(BaseNotifier):
    def __init__(self):
        self.name = 'Bark App'
        self.token = config.BARK_KEY
        self.retcode_key = 'code'
        self.retcode_value = 200
    
    def send(self, text, status, desp):
        from config import PUSH_CONFIG

        if not PUSH_CONFIG:
            return log.info(f'自定义推送 🚫')

        cust = to_python(PUSH_CONFIG)
        title = f'{text} {status}'

        if cust['merge_title_and_desp']:
            title = f'{text} {status}\n\n{desp}'
        if cust['set_data_title'] and cust['set_data_sub_title']:
            cust['data'][cust['set_data_title']] = {
                cust['set_data_sub_title']: title
            }
        elif cust['set_data_title'] and cust['set_data_desp']:
            cust['data'][cust['set_data_title']] = title
            cust['data'][cust['set_data_desp']] = desp
        elif cust['set_data_title']:
            cust['data'][cust['set_data_title']] = title

        url, data, name, retcode_key, retcode_value = [
            cust['url'], cust['data'], '自定义推送', cust['retcode_key'],
            cust['retcode_value']
        ]

        if cust['method'].upper() == 'GET':
            return self.push(
                'get',
                url,
                params=data,
                name=name,
                token='token',
                retcode_key=retcode_key,
                retcode_value=retcode_value)
        elif cust['method'].upper() == 'POST' and cust['data_type'].lower(
        ) == 'json':
            return self.push(
                'post',
                url,
                json=data,
                name=name,
                token='token',
                retcode_key=retcode_key,
                retcode_value=retcode_value)
        else:
            return self.push(
                'post',
                url,
                data=data,
                name=name,
                token='token',
                retcode_key=retcode_key,
                retcode_value=retcode_value)
 
