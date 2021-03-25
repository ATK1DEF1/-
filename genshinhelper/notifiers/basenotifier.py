from ..utils import log, req


class BaseNotifier(object):
    def __init__(self):
        self.name = ''
        self.token = ''
        self.retcode_key = ''
        self.retcode_value = ''

    def send(self, text, status, desp):
        ...

    def push(self,
             method,
             url,
             params=None,
             data=None,
             json=None,
             headers=None,
             **kwargs):
        """
        🚫: disabled; 🥳:success; 😳:failure
        """
        if not self.token:
            log.info(f'{self.name} 🚫')
            return
        try:
            response = req.request(method, url, 2, params, data, json,
                                   headers).json()
        except Exception as e:
            log.error(f'{self.name} 😳\n{e}')
        else:
            retcode = response.get(self.retcode_key, -1)
            if retcode == self.retcode_value:
                log.info(f'{self.name} 🥳')
            # Telegram Bot
            elif self.name == 'Telegram Bot' and retcode:
                log.info(f'{self.name} 🥳')
            elif self.name == 'Telegram Bot' and response[self.
                                                          retcode_value] == 400:
                log.error(f'{self.name} 😳\n请主动给 bot 发送一条消息并检查 TG_USER_ID 是否正确')
            elif self.name == 'Telegram Bot' and response[self.
                                                          retcode_value] == 401:
                log.error(f'{self.name} 😳\nTG_BOT_TOKEN 错误')
            else:
                log.error(f'{self.name} 😳\n{response}')
