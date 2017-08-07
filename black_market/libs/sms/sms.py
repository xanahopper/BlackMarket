from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

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
