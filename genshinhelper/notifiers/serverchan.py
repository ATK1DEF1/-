from .basenotifier import BaseNotifier


class ServerChan(BaseNotifier):
    def notify(self, text, status, desp):
        from config import SCKEY

        url = f'https://sc.ftqq.com/{SCKEY}.send'
        data = {'text': f'{text} {status}', 'desp': desp}
        name, token, retcode_key, retcode_value = ['Server酱', SCKEY, 'errno', 0]
        return self.push(
            'post',
            url,
            data=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

