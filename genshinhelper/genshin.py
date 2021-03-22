"""Genshin Impact Helper.
Automatically get Genshin Impact daily check-in rewards.

Github:
    https://github.com/y1ndan/genshin-impact-helper
"""
import hashlib
import time
import random
import string
import uuid
import json

from functools import wraps

from .utils import CONFIG, log, req

from genshinhelper import config


def hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def _data_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if 'Yuanshen' in self.__class__.__name__:
            self.get_roles()
            roles = self._roles_info
            if roles and (roles.get('retcode', 1) != 0 or not roles.get('data')):
                raise Exception(roles.get('message', 'Empty roles data'))
            role_list = roles.get('data', {}).get('list', [])
            if roles and not role_list:
                raise Exception(roles.get('message', 'Empty roles list'))
            if role_list:
                result_list = []
                log.info(f'当前账号绑定了 {len(role_list)} 个角色')
                for role in role_list:
                    # cn_gf01:  天空岛
                    # cn_qd01:  世界树
                    region = role.get('region', 'cn')
                    region_name = role.get('region_name', 'CN')
                    uid = role.get('game_uid', 123456789)
                    self._info_url = self.info_url.format(
                        region, self._act_id, uid)
                    post_data = {
                        'act_id': self._act_id,
                        'region': region,
                        'uid': uid
                    }
                    self._sign_data.update({
                        'region_name': region_name,
                        'uid': uid,
                        'post_data': post_data
                    })
                    result_list.append(func(self, *args, **kwargs))
                return ''.join(result_list)
        elif 'Genshin' in self.__class__.__name__:
            try:
                self._sign_data['uid'] = self._cookie.split('account_id=')[
                    1].split(';')[0]
            except Exception as e:
                raise Exception(e)
            self._sign_data['post_data'] = {'act_id': self._act_id}
            return func(self, *args, **kwargs)
    return wrapper


class __BaseCheckin(object):
    def __init__(self, cookie: str = None):
        self._cookie = cookie
        self._sign_info = {}
        self._rewards_info = {}
        self._sign_data = {}
        self._init_sign_config()

    def _init_sign_config(self):
        ...

    def get_header(self):
        header = {
            'Cookie': self._cookie,
            'User-Agent': self._user_agent,
            'Referer': self._referer,
            'Accept-Encoding': 'gzip, deflate, br'
        }
        return header

    def get_sign_info(self):
        try:
            self._sign_info = req.request(
                'get', self._info_url, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        return self._sign_info

    def get_rewards(self):
        try:
            self._rewards_info = req.request(
                'get', self._reward_url, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        return self._rewards_info

    @_data_handler
    def run(self):
        if not self._sign_info:
            self.get_sign_info()
        if not self._rewards_info:
            self.get_rewards()

        today = self._sign_info.get('data', {}).get('today', '1970-01-01')
        total_sign_day = self._sign_info.get('data', {}).get(
            'total_sign_day', 0)
        is_sign = self._sign_info.get('data', {}).get('is_sign')
        first_bind = self._sign_info.get('data', {}).get('first_bind')
        awards = self._rewards_info.get('data', {}).get('awards', [])
        region_name = self._sign_data.get('region_name', 'Global')
        uid = self._sign_data.get('uid', 123456789)
        hidden_uid = str(uid).replace(str(uid)[2:-2], '*****', 1)
        data = self._sign_data.get('post_data', {})

        message = {
            'today': today,
            'region_name': region_name,
            'uid': hidden_uid,
            'total_sign_day': total_sign_day,
            'end': ''
        }

        log.info(f'准备为旅行者 {hidden_uid} 签到...')
        time.sleep(1)

        if is_sign:
            message['award_name'] = awards[total_sign_day - 1].get('name')
            message['award_cnt'] = awards[total_sign_day - 1].get('cnt')
            message['status'] = '👀 旅行者, 你已经签到过了哦'

            # return ''.join(self.message.format(**message))
            return self.message.format(**message)
        else:
            message['award_name'] = awards[total_sign_day].get('name')
            message['award_cnt'] = awards[total_sign_day].get('cnt')
        if first_bind:
            message['status'] = '💪 旅行者, 请先手动签到一次'

            return self.message.format(**message)

        try:
            response = req.request('post', self._sign_url, headers=self.get_header(
            ), data=json.dumps(data, ensure_ascii=False)).json()
        except Exception as e:
            raise Exception(e)
        # 0:      success
        # -5003:  already checked in
        code = response.get('retcode', 99999)
        if code != 0:
            return response
        message['total_sign_day'] = total_sign_day + 1
        message['status'] = response.get('message')

        log.info('签到完毕')
        return self.message.format(**message)

    @property
    def message(self):
        return CONFIG.MESSAGE_TEMPLATE


class YuanshenCheckin(__BaseCheckin):
    def _init_sign_config(self):
        self._app_version = '2.3.0'
        self._act_id = 'e202009291139501'
        self._user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/{}'.format(
            self._app_version)
        self._referer = 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required={}&act_id={}&utm_source={}&utm_medium={}&utm_campaign={}'.format(
            'true', self._act_id, 'bbs', 'mys', 'icon')
        self._role_url = 'https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={}'.format(
            'hk4e_cn')
        self._roles_info = {}
        self._info_url = ''
        self.info_url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?region={}&act_id={}&uid={}'
        self._reward_url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id={}'.format(
            self._act_id)
        self._sign_url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign'

    @property
    def get_ds(self):
        # v2.3.0-web @povsister & @journey-ad
        n = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl'
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = hexdigest(f'salt={n}&t={i}&r={r}')
        return f'{i},{r},{c}'

    def get_header(self):
        header = super().get_header()
        header.update({
            'x-rpc-device_id': str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper(),
            # 1:  ios
            # 2:  android
            # 4:  pc web
            # 5:  mobile web
            'x-rpc-client_type': '5',
            'x-rpc-app_version': self._app_version,
            'DS': self.get_ds
        })
        return header

    def get_roles(self):
        try:
            self._roles_info = req.request(
                'get', self._role_url, headers=super().get_header()).json()
        except Exception as e:
            raise Exception(e)
        return self._roles_info


class GenshinCheckin(__BaseCheckin):
    def _init_sign_config(self):
        self._act_id = 'e202102251931481'
        self._user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        self._referer = 'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={}'.format(
            self._act_id)
        self._info_url = 'https://hk4e-api-os.mihoyo.com/event/sol/info?lang={}&act_id={}'.format(
            config.LANGUAGE, self._act_id)
        self._reward_url = 'https://hk4e-api-os.mihoyo.com/event/sol/home?lang={}&act_id={}'.format(
            config.LANGUAGE, self._act_id)
        self._sign_url = 'https://hk4e-api-os.mihoyo.com/event/sol/sign?lang={}'.format(
            config.LANGUAGE)

