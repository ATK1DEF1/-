from ..utils import log, req


class BaseNotifier(object):
    """
    🚫: disabled; 🥳:success; 😳:failure
    """

    def push(self,
             method,
             url,
             params=None,
             data=None,
             json=None,
             headers=None,
             **kwargs):
        name = kwargs.get('name')
        token = kwargs.get('token')
        retcode_key = kwargs.get('retcode_key')
        retcode_value = kwargs.get('retcode_value')

        if not token:
            log.info(f'{name} 🚫')
            return
        try:
            response = req.request(
                method, url, 2, params, data, json, headers).json()
        except Exception as e:
            log.error(f'{name} 😳\n{e}')
        else:
            retcode = response.get(retcode_key, -1)
            if retcode == retcode_value:
                log.info(f'{name} 🥳')
            # Telegram Bot
            elif name == 'Telegram Bot' and retcode:
                log.info(f'{name} 🥳')
            elif name == 'Telegram Bot' and response[retcode_value] == 400:
                log.error(f'{name} 😳\n请主动给 bot 发送一条消息并检查 TG_USER_ID 是否正确')
            elif name == 'Telegram Bot' and response[retcode_value] == 401:
                log.error(f'{name} 😳\nTG_BOT_TOKEN 错误')
            else:
                log.error(f'{name} 😳\n{response}')
