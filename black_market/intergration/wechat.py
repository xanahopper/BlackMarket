import requests
from flask import make_response

from black_market.config import WEIXIN_APP_ID, WEIXIN_APP_SECRET
from black_market.model.exceptions import WeChatServiceError

JSCODE2SESSION_URL = 'https://api.weixin.qq.com/sns/jscode2session'
GET_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
GET_APP_QRCOODE_URL = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={access_token}'


class Wechat(object):

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def jscode2session(self, code, grant_type='authorization_code'):
        params = dict(appid=self.app_id, secret=self.app_secret,
                      js_code=code, grant_type=grant_type)
        return requests.get(JSCODE2SESSION_URL, params=params)

    def get_access_token(self, grant_type='client_credential'):
        params = dict(appid=self.app_id, secret=self.app_secret, grant_type=grant_type)
        r = requests.get(GET_ACCESS_TOKEN_URL, params=params)
        if r.status_code == 200:
            access_token = r.json().get('access_token')
            return access_token
        raise WeChatServiceError()

    def get_app_qrcode_by_path(self, path):
        access_token = self.get_access_token()
        json = dict(path=path)
        url = GET_APP_QRCOODE_URL.format(access_token=access_token)
        r = requests.post(url, json=json)
        res = make_response(r.content)
        res.headers['Content-Type'] = r.headers['Content-Type']
        return res

wechat = Wechat(WEIXIN_APP_ID, WEIXIN_APP_SECRET)
