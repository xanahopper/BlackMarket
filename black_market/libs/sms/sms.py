import requests
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

from task.celery import app
from black_market.config import SMS_YUNPIAN_APIKEY, DEBUG


class SMS(object):

    @classmethod
    def send(cls, number, message, tag):
        if DEBUG:
            print('{number}\t{message}\t{tag}'.format(
                number=number,
                message=message,
                tag=tag
            ))
            return
        return cls._yunpian_sender(number, message, tag)

    @classmethod
    def _yunpian_sender(cls, number, message, tag):
        client = YunpianClient(SMS_YUNPIAN_APIKEY)
        param = {YC.MOBILE: number, YC.TEXT: message}
        r = client.sms().single_send(param)

        if r.code() == 200:
            r = r.json()
            code = r.get('code')
            # msg = r.get('msg')
            # sid = r.get('sid') or ''
            try:
                if int(code) == 0:
                    return True
            except:
                return False
        return False

    @staticmethod
    @app.task
    def reg_complete(mobile):
        url = 'https://sms.yunpian.com/v2/sms/reg_complete.json'
        json = dict(apikey=SMS_YUNPIAN_APIKEY, mobile=mobile)
        try:
            requests.post(url, json=json)
        except Exception:
            pass
