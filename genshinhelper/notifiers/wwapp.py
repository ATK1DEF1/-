from .basenotifier import BaseNotifier
from ..utils import log, req, to_python


class WwApp(BaseNotifier):
    def get_wwtoken(self):
        from config import WW_ID, WW_APP_SECRET

        if WW_ID and WW_APP_SECRET:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
            data = {'corpid': WW_ID, 'corpsecret': WW_APP_SECRET}

            try:
                response = to_python(req.request('get', url, params=data).text)
            except Exception as e:
                log.error(e)
            else:
                retcode = response.get('errcode')
                if retcode == 0:
                    log.info('access_token 获取成功')
                    return response['access_token']
                else:
                    log.error(f'access_token 获取失败:\n{response}')
        else:
            log.info('企业微信应用 🚫')

    def notify(self, text, status, desp):
        from config import WW_APP_USERID, WW_APP_AGENTID

        token = ''
        if WW_APP_USERID and WW_APP_AGENTID:
            token = 'token'
        access_token = self.get_wwtoken()

        if access_token:
            url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
            data = {
                'touser': WW_APP_USERID,
                'msgtype': 'text',
                'agentid': WW_APP_AGENTID,
                'text': {
                    'content': f'{text} {status}\n\n{desp}'
                }
            }
            name, token, retcode_key, retcode_value = [
                '企业微信应用', token, 'errcode', 0
            ]
        return self.push(
            'post',
            url,
            json=data,
            name=name,
            token=token,
            retcode_key=retcode_key,
            retcode_value=retcode_value)

