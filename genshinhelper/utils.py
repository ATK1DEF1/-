"""Utilities."""

import logging
import json
import hashlib
import time
import random
import string

import requests
from requests.exceptions import HTTPError


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

log = logger = logging


class _Config:

    # weibo
    CONTAINER_ID = '100808fc439dedbb06ca5fd858848e521b8716'
    WB_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    SUPER_URL = 'https://m.weibo.cn/api/container/getIndex?containerid={}'.format(
        '100803_-_page_my_follow_super')
    YS_URL = 'https://m.weibo.cn/api/container/getIndex?containerid={}_-_feed'.format(
        CONTAINER_ID)
    KA_URL = 'https://ka.sina.com.cn/innerapi/draw'
    BOX_URL = 'https://ka.sina.com.cn/html5/mybox'


class HttpRequest(object):
    def request(self,
                method: str,
                url: str,
                max_retry: int = 2,
                params=None,
                data=None,
                json=None,
                headers=None,
                **kwargs):
        for i in range(max_retry + 1):
            try:
                response = requests.Session().request(
                    method,
                    url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                    **kwargs)
            except HTTPError as e:
                log.error(f'HTTP error:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            except KeyError as e:
                log.error(f'Wrong response:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            except Exception as e:
                log.error(f'Unknown error:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            else:
                return response

        raise Exception(f'All {max_retry + 1} HTTP requests failed, die.')


def get_accounts(cookies):
    if '#' in cookies:
        return cookies.split('#')
    else:
        return cookies.splitlines()


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🔅[{region_name}]{uid}
    今日奖励: {award_name} × {award_cnt}
    本月累签: {total_sign_day} 天
    签到结果: {status}
    {end:#^18}'''

req = HttpRequest()
CONFIG = _Config
CONFIG.MESSAGE_TEMPLATE = MESSAGE_TEMPLATE
