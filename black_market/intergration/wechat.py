import time
import random

import base36
from werkzeug.utils import cached_property
from wechatpy.oauth import WeChatOAuth
from wechatpy.client import WeChatClient
from wechatpy.session.redisstorage import RedisStorage

from black_market.libs.cache.redis import mc
from black_market.config import WEIXIN_APP_ID, WEIXIN_APP_SECRET


class Wechat(object):

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    @cached_property
    def oauth(self):
        return WeChatOAuth(self.app_id, self.app_secret, '')

    @cached_property
    def client(self):
        return WeChatClient(self.app_id, self.app_secret, session=RedisStorage(redis=mc))

    @property
    def jsapi_ticket(self):
        return self.client.jsapi.get_jsapi_ticket()

    def get_jsapi_config(self, url, **kwargs):
        noncestr = base36.dumps(random.randint(1e50, 9e50))
        timestamp = int(time.time())

        signature = self.client.jsapi.get_jsapi_signature(
            noncestr=noncestr,
            ticket=self.jsapi_ticket,
            timestamp=timestamp,
            url=url
        )

        config = {
            'appId': self.app_id,
            'timestamp': timestamp,
            'nonceStr': noncestr,
            'signature': signature,
            'jsApiList': []}
        config.update(**kwargs)
        return config

wechat = Wechat(WEIXIN_APP_ID, WEIXIN_APP_SECRET)
