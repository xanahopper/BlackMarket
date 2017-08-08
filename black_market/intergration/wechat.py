import requests

# import base36
# from werkzeug.utils import cached_property

# from black_market.libs.cache.redis import mc
from black_market.config import WEIXIN_APP_ID, WEIXIN_APP_SECRET


JSCODE2SESSION_URL = 'https://api.weixin.qq.com/sns/jscode2session'


class Wechat(object):

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def jscode2session(self, code, grant_type='authorization_code'):
        params = dict(appid=self.app_id, secret=self.app_secret,
                      js_code=code, grant_type=grant_type)
        return requests.get(JSCODE2SESSION_URL, params=params)


wechat = Wechat(WEIXIN_APP_ID, WEIXIN_APP_SECRET)
