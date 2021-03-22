from .basenotifier import BaseNotifier


class CoolPush(BaseNotifier):
    def notify(self, text, status, desp):
        from config import COOL_PUSH_SKEY, COOL_PUSH_MODE

        url = f'https://push.xuthus.cc/{COOL_PUSH_MODE}/{COOL_PUSH_SKEY}'
        data = f'{text} {status}\n\n{desp}'.encode('utf-8')
        name, token, retcode_key, retcode_value = [
            'Cool Push', COOL_PUSH_SKEY, 'code', 200
        ]
        return self.push(
            'post',
            url,
            data=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

