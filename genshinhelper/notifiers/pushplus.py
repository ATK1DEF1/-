from .basenotifier import BaseNotifier


class PushPlus(BaseNotifier):
    def notify(self, text, status, desp):
        from config import PUSH_PLUS_TOKEN, PUSH_PLUS_USER

        url = 'https://pushplus.hxtrip.com/send'
        data = {
            'token': PUSH_PLUS_TOKEN,
            'title': f'{text} {status}',
            'content': desp,
            'topic': PUSH_PLUS_USER
        }
        name, token, retcode_key, retcode_value = [
            'pushplus', PUSH_PLUS_TOKEN, 'code', 200
        ]
        return self.push(
            'post',
            url,
            data=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

