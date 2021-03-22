"""Configuration

Note:   Github Actions users please go to
repo's Settings->Secrets to set the variables, the name of the variable
MUST be the same as the key in the config.json file,
otherwise it is invalid!!!

e.g. Name=COOKIE, Value=<cookie>
"""

import os
import json


class Config:
    """
    Get all configuration from the config.json file.

    Note:   Environment variables have a higher priority, if you set a environment variable in your system, that variable in the config.json file will be invalid.
    """

    def __init__(self):
        # Open and read the config file
        CONFIG_DIR = './config.json'
        with open(CONFIG_DIR, 'r', encoding='utf-8') as f:
            config_json = json.load(f)

        # Language
        self.LANGUAGE = config_json['LANGUAGE']

        # Cookie configs
        # Cookie from https://bbs.mihoyo.com/ys/
        self.COOKIE = config_json['COOKIE']
        # Cookie from https://www.hoyolab.com/genshin/
        self.COOKIE_HOYOLAB = config_json['COOKIE_HOYOLAB']
        # Cookie from https://m.weibo.cn
        self.COOKIE_WB = config_json['COOKIE_WB']
        # Cookie from https://ka.sina.com.cn
        self.COOKIE_KA = config_json['COOKIE_KA']

        # Notifier configs
        # Server Chan
        self.SCKEY = config_json['SCKEY']
        self.SCTKEY = config_json['SCTKEY']
        # Cool Push
        self.COOL_PUSH_SKEY = config_json['COOL_PUSH_SKEY']
        self.COOL_PUSH_MODE = config_json['COOL_PUSH_MODE']
        # iOS Bark App
        self.BARK_KEY = config_json['BARK_KEY']
        self.BARK_SOUND = config_json['BARK_SOUND']
        # Discord webhook
        self.DISCORD_WEBHOOK = config_json['DISCORD_WEBHOOK']
        # Telegram Bot
        self.TG_BOT_API = config_json['TG_BOT_API']
        self.TG_BOT_TOKEN = config_json['TG_BOT_TOKEN']
        self.TG_USER_ID = config_json['TG_USER_ID']
        # DingTalk Bot
        self.DD_BOT_TOKEN = config_json['DD_BOT_TOKEN']
        self.DD_BOT_SECRET = config_json['DD_BOT_SECRET']
        # WeChat Work Bot
        self.WW_BOT_KEY = config_json['WW_BOT_KEY']
        # WeChat Work App
        self.WW_ID = config_json['WW_ID']
        self.WW_APP_SECRET = config_json['WW_APP_SECRET']
        self.WW_APP_USERID = config_json['WW_APP_USERID']
        self.WW_APP_AGENTID = config_json['WW_APP_AGENTID']
        # iGot
        self.IGOT_KEY = config_json['IGOT_KEY']
        # pushplus
        self.PUSH_PLUS_TOKEN = config_json['PUSH_PLUS_TOKEN']
        self.PUSH_PLUS_USER = config_json['PUSH_PLUS_USER']
        # Custom Push Config
        self.CUSTOM_PUSH_CONFIG = config_json['CUSTOM_PUSH_CONFIG']

        # Get configuration from user's environment variables
        if 'LANGUAGE' in os.environ:
            self.LANGUAGE = os.environ['LANGUAGE']

        if 'COOKIE' in os.environ:
            self.COOKIE = os.environ['COOKIE']
        if 'COOKIE_HOYOLAB' in os.environ:
            self.COOKIE_HOYOLAB = os.environ['COOKIE_HOYOLAB']
        if 'COOKIE_WB' in os.environ:
            self.COOKIE_WB = os.environ['COOKIE_WB']
        if 'COOKIE_KA' in os.environ:
            self.COOKIE_KA = os.environ['COOKIE_KA']

        if 'SCKEY' in os.environ:
            self.SCKEY = os.environ['SCKEY']
        if 'SCTKEY' in os.environ:
            self.SCTKEY = os.environ['SCTKEY']
        if 'COOL_PUSH_SKEY' in os.environ:
            self.COOL_PUSH_SKEY = os.environ['COOL_PUSH_SKEY']
        if 'COOL_PUSH_MODE' in os.environ:
            self.COOL_PUSH_MODE = os.environ['COOL_PUSH_MODE']
        if 'BARK_KEY' in os.environ:
            # Customed server
            if os.environ['BARK_KEY'].find(
                    'https') != -1 or os.environ['BARK_KEY'].find('http') != -1:
                self.BARK_KEY = os.environ['BARK_KEY']
            else:
                self.BARK_KEY = f"https://api.day.app/{os.environ['BARK_KEY']}"
        # Official server
        elif self.BARK_KEY and self.BARK_KEY.find('https') == -1 and self.BARK_KEY.find('http') == -1:
            self.BARK_KEY = f'https://api.day.app/{self.BARK_KEY}'
        if 'BARK_SOUND' in os.environ:
            self.BARK_SOUND = os.environ['BARK_SOUND']
        if 'DSCORD_WEBHOOK' in os.environ:
            self.DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']
        if 'TG_BOT_API' in os.environ:
            self.TG_BOT_API = os.environ['TG_BOT_API']
        if 'TG_BOT_TOKEN' in os.environ:
            self.TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
        if 'TG_USER_ID' in os.environ:
            self.TG_USER_ID = os.environ['TG_USER_ID']
        if 'DD_BOT_TOKEN' in os.environ:
            self.DD_BOT_TOKEN = os.environ['DD_BOT_TOKEN']
        if 'DD_BOT_SECRET' in os.environ:
            self.DD_BOT_SECRET = os.environ['DD_BOT_SECRET']
        if 'WW_BOT_KEY' in os.environ:
            self.WW_BOT_KEY = os.environ['WW_BOT_KEY']
        if 'WW_ID' in os.environ:
            self.WW_ID = os.environ['WW_ID']
        if 'WW_APP_SECRET' in os.environ:
            self.WW_APP_SECRET = os.environ['WW_APP_SECRET']
        if 'WW_APP_USERID' in os.environ:
            self.WW_APP_USERID = os.environ['WW_APP_USERID']
        if 'WW_APP_AGENTID' in os.environ:
            self.WW_APP_AGENTID = os.environ['WW_APP_AGENTID']
        if 'IGOT_KEY' in os.environ:
            self.IGOT_KEY = os.environ['IGOT_KEY']
        if 'PUSH_PLUS_TOKEN' in os.environ:
            self.PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
        if 'PUSH_PLUS_USER' in os.environ:
            self.PUSH_PLUS_USER = os.environ['PUSH_PLUS_USER']
        if 'CUSTOM_PUSH_CONFIG' in os.environ:
            self.CUSTOM_PUSH_CONFIG = os.environ['CUSTOM_PUSH_CONFIG']

