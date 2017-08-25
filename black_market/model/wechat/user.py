import pickle
from datetime import datetime

from black_market.ext import db
from black_market.libs.cache.redis import mc, ONE_DAY


class WechatUser(db.Model):
    __tablename__ = 'wechat_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(80), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(80))
    avatar_url = db.Column(db.String(256))
    city = db.Column(db.String(80))
    country = db.Column(db.String(80))
    gender = db.Column(db.SmallInteger)
    language = db.Column(db.String(80))
    province = db.Column(db.String(80))
    create_time = db.Column(db.DateTime(), default=datetime.now())
    update_time = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())

    _cache_key_prefix = 'wechat_user:'
    _wechat_user_by_open_id_cache_key = _cache_key_prefix + 'open_id:%s'

    def __init__(self, open_id, nickname, avatar_url, city,
                 country, gender, language, province, update_time):
        self.open_id = open_id
        self.nickname = nickname
        self.avatar_url = avatar_url
        self.city = city
        self.country = country
        self.gender = gender
        self.language = language
        self.province = province
        self.update_time = update_time

    @classmethod
    def add(cls, open_id, nickname, avatar_url, city,
            country, gender, language, province):
        instance = cls.get_by_open_id(open_id)
        if instance:
            instance.update(nickname, avatar_url, city, country,
                            gender, language, province)
            return instance.id

        update_time = datetime.now()
        wechat_user = WechatUser(
            open_id, nickname, avatar_url, city,
            country, gender, language, province, update_time)

        db.session.add(wechat_user)
        db.session.commit()
        return wechat_user.id

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_open_id(cls, open_id):
        cache_key = cls._wechat_user_by_open_id_cache_key % open_id
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        wechat_user = cls.query.filter_by(open_id=open_id).first()
        if wechat_user:
            mc.set(cache_key, pickle.dumps(wechat_user).hex())
            mc.expire(cache_key, ONE_DAY)
        return wechat_user

    def update(self, nickname, avatar_url, city, country,
               gender, language, province):
        self.nickname = nickname
        self.avatar_url = avatar_url
        self.city = city
        self.country = country
        self.gender = gender
        self.language = language
        self.province = province
        self.update_time = datetime.now()
        db.session.add(self)
        db.session.commit()
        self.clear_cache()

    def delete(self):
        self.clear_cache()
        db.session.delete(self)
        db.session.commit()

    def clear_cache(self):
        mc.delete(self._wechat_user_by_open_id_cache_key % self.open_id)
