from .basenotifier import BaseNotifier


class TgBot(BaseNotifier):
    def notify(self, text, status, desp):
        from config import TG_BOT_TOKEN, TG_USER_ID
        token = ''
        if TG_BOT_TOKEN and TG_USER_ID:
            token = 'token'

        url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': TG_USER_ID,
            'text': f'{text} {status}\n\n{desp}',
            'disable_web_page_preview': True
        }
        name, token, retcode_key, retcode_value = [
            'Telegram Bot', token, 'ok', 'error_code'
        ]
        return self.push(
            'post',
            url,
            data=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

