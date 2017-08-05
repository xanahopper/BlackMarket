import uuid
from datetime import datetime, timedelta

from black_market.ext import db
from black_market.libs.cache.redis import mc


class WechatOAuthToken(db.Model):
    __tablename__ = 'wechat_oauth_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nonce = db.Column(db.String(80), unique=True)
    open_id = db.Column(db.String(80))
    access_token = db.Column(db.String(80))
    refresh_token = db.Column(db.String(80))
    scopes = db.Column(db.String(80))
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    expire_time = db.Column(db.DateTime())

    _cache_key_prefix = 'wechat_oauth_token:'
    _token_cache_key = _cache_key_prefix + 'id:%s'
    _id_by_open_id_cache_key = _cache_key_prefix + 'open_id:%s'
    _id_by_token_type_and_value_cache_key = _cache_key_prefix + 'type:%s:value:%s'

    def __init__(self, nonce, open_id, access_token, refresh_token, scopes, expire_time):
        self.nonce = nonce
        self.open_id = open_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scopes = scopes.split(',')
        self.expire_time = expire_time

    @classmethod
    def add(cls, open_id, access_token, refresh_token, scopes, expires_in):
        nonce = uuid.uuid4().hex
        instance = cls.get_by_open_id(open_id)
        if instance:
            instance.update(nonce, access_token, refresh_token, scopes, expires_in)
            return instance.id_

        expire_time = datetime.now() + timedelta(seconds=expires_in)
        wechat_oauth_token = WechatOAuthToken(
            nonce, open_id, access_token, refresh_token, scopes, expire_time)

        db.session.add(wechat_oauth_token)
        db.session.commit()

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_nonce(cls, nonce):
        return cls.query.filter_by(nonce=nonce).first()

    @classmethod
    def get_by_open_id(cls, open_id):
        return cls.query.filter_by(open_id=open_id).first()

    def update(self, nonce, access_token, refresh_token, scopes, expires_in):
        self.nonce = nonce
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scopes = scopes
        self.expire_time = datetime.now() + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        self.clear_cache()

    def invalidate_nonce(self):
        self.nonce = uuid.uuid4().hex
        db.session.add(self)
        db.session.commit()
        self.clear_cache()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        self.clear_cache()

    def clear_cache(self):
        mc.delete(self._token_cache_key % self.id_)
        mc.delete(self._id_by_open_id_cache_key % self.open_id)
