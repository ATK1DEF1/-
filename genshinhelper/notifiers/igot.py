from .basenotifier import BaseNotifier


class Igot(BaseNotifier):
    def notify(self, text, status, desp):
        from config import IGOT_KEY

        url = f'https://push.hellyw.com/{IGOT_KEY}'
        data = {'title': f'{text} {status}', 'content': desp}
        name, token, retcode_key, retcode_value = ['iGot', IGOT_KEY, 'ret', 0]
        return self.push(
            'post',
            url,
            data=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

