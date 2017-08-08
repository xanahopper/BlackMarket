from datetime import datetime, timedelta

from black_market.ext import db
# from black_market.libs.cache.redis import mc


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
    create_time = db.Column(db.DateTime(), default=datetime.utcnow())
    expire_time = db.Column(db.DateTime())

    # _cache_key_prefix = 'wechat_user_info:'
    # _token_cache_key = _cache_key_prefix + 'id:%s'
    # _id_by_open_id_cache_key = _cache_key_prefix + 'open_id:%s'

    def __init__(self, open_id, nickname, avatar_url, city,
                 country, gender, language, province, expire_time):
        self.open_id = open_id
        self.nickname = nickname
        self.avatar_url = avatar_url
        self.city = city
        self.country = country
        self.gender = gender
        self.language = language
        self.province = province
        self.expire_time = expire_time

    @classmethod
    def add(cls, open_id, nickname, avatar_url, city,
            country, gender, language, province, expires_in=1800):
        instance = cls.get_by_open_id(open_id)
        if instance:
            instance.update(nickname, avatar_url, city, country,
                            gender, language, province, expires_in)
            return instance.id

        expire_time = datetime.now() + timedelta(seconds=expires_in)
        wechat_session = WechatUser(
            open_id, nickname, avatar_url, city,
            country, gender, language, province, expire_time)

        db.session.add(wechat_session)
        db.session.commit()
        return wechat_session.id

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_open_id(cls, open_id):
        return cls.query.filter_by(open_id=open_id).first()

    def update(self, nickname, avatar_url, city, country,
               gender, language, province, expires_in):
        self.nickname = nickname
        self.avatar_url = avatar_url
        self.city = city
        self.country = country
        self.gender = gender
        self.language = language
        self.province = province
        self.expire_time = datetime.now() + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        # self.clear_cache()

    # def clear_cache(self):
    #     mc.delete(self._token_cache_key % self.id_)
    #     mc.delete(self._id_by_open_id_cache_key % self.open_id)
