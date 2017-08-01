import requests

from black_market.config import SMS_YUNPIAN_HTTP, SMS_YUNPIAN_APIKEY, DEBUG


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
        api = SMS_YUNPIAN_HTTP
        mobile = number
        data = dict(apikey=SMS_YUNPIAN_APIKEY, mobile=mobile, text=message)
        r = requests.post(api, data)
        if r.status_code == 200:
            r = r.json()
            code = r.get('code')
            msg = r.get('msg')
            sid = r.get('sid') or ''
            try:
                if int(code) == 0:
                    return True
            except:
                return False
        return False
