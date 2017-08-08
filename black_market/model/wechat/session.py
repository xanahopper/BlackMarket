import uuid
from datetime import datetime, timedelta

from black_market.ext import db
# from black_market.libs.cache.redis import mc


class WechatSession(db.Model):
    __tablename__ = 'wechat_session'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(80), index=True, nullable=False)
    session_key = db.Column(db.String(80), nullable=False)
    third_session_key = db.Column(db.String(80), unique=True, index=True, nullable=False)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow())
    expire_time = db.Column(db.DateTime())

    # _cache_key_prefix = 'wechat_session:'
    # _token_cache_key = _cache_key_prefix + 'id:%s'
    # _id_by_open_id_cache_key = _cache_key_prefix + 'open_id:%s'

    def __init__(self, open_id, session_key, third_session_key, expire_time):
        self.open_id = open_id
        self.session_key = session_key
        self.third_session_key = third_session_key
        self.expire_time = expire_time

    @classmethod
    def add(cls, open_id, session_key, expires_in=1800):
        third_session_key = uuid.uuid4().hex
        instance = cls.get_by_open_id(open_id)
        if instance:
            instance.update(session_key, third_session_key, expires_in)
            return third_session_key

        expire_time = datetime.now() + timedelta(seconds=expires_in)
        wechat_session = WechatSession(
            open_id, session_key, third_session_key, expire_time)

        db.session.add(wechat_session)
        db.session.commit()
        return third_session_key

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_third_session_key(cls, third_session_key):
        wechat_session = cls.query.filter_by(third_session_key=third_session_key).first()
        if wechat_session and not wechat_session.expired:
            return wechat_session
        return None

    @classmethod
    def get_by_open_id(cls, open_id):
        return cls.query.filter_by(open_id=open_id).first()

    @property
    def expired(self):
        return bool(datetime.utcnow() > self.expire_time)

    @property
    def wechat_user(self):
        from black_market.model.wechat.user import WechatUser
        return WechatUser.get_by_open_id(self.open_id)

    def update(self, session_key, third_session_key, expires_in):
        self.session_key = session_key
        self.third_session_key = third_session_key
        self.expire_time = datetime.now() + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        # self.clear_cache()

    def invalidate_third_session_key(self):
        self.third_session_key = uuid.uuid4().hex
        db.session.add(self)
        db.session.commit()
        # self.clear_cache()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        # self.clear_cache()

    # def clear_cache(self):
    #     mc.delete(self._token_cache_key % self.id_)
    #     mc.delete(self._id_by_open_id_cache_key % self.open_id)
