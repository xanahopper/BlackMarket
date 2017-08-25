import pickle
from datetime import datetime

from black_market.ext import db
from black_market.libs.cache.redis import mc, rd, ONE_HOUR
from black_market.model.user.student import Student
from black_market.model.user.view_record import ViewRecord
from black_market.model.post.consts import PostStatus, OrderType, PostType
from black_market.model.utils.crypto import decrypt, encrypt
from black_market.model.exceptions import CannotEditPostError


class GoodsPost(db.Model):
    __tablename__ = 'goods_post'

    _cache_key_prefix = 'goods:post:'
    _goods_post_by_id_cache_key = _cache_key_prefix + 'id:%s'
    _post_pv_by_id_cache_key = _cache_key_prefix + 'pv:id:%s'

    MAX_EDIT_TIMES = 5

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    status_ = db.Column(db.SmallInteger)
    switch = db.Column(db.SmallInteger)
    mobile = db.Column(db.String(80))
    wechat = db.Column(db.String(80))
    message = db.Column(db.String(256))
    imgs = db.Column(db.String(80))
    pv_ = db.Column(db.Integer, default=0)
    editable = db.Column(db.SmallInteger, default=MAX_EDIT_TIMES)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, student_id, switch, mobile, wechat, message, imgs, status=PostStatus.normal):
        self.student_id = student_id
        self.switch = switch.value
        self.mobile = mobile
        self.wechat = wechat
        self.message = message
        self.imgs = imgs
        self.status_ = status.value

    def dump(self):
        return dict(
            id=self.id, student=self.student.dump(), switch=self.switch, mobile=self.mobile,
            wechat=self.wechat, message=self.message, pv=self.pv, status=self.status_,
            editable=self.editable, create_time=self.create_time, update_time=self.update_time,
            fuzzy_id=self.fuzzy_id)

    def share_dump(self):
        return dict(
            id=self.id, student=self.student.share_dump(), message=self.message,
            pv=self.pv, status=self.status_, create_time=self.create_time,
            update_time=self.update_time)

    @classmethod
    def get(cls, id_):
        cache_key = cls._goods_post_by_id_cache_key % id_
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        post = GoodsPost.query.get(id_)
        if post:
            mc.set(cache_key, pickle.dumps(post).hex())
            mc.expire(cache_key, ONE_HOUR)
        return post

    @classmethod
    def gets(cls, limit=5, offset=0, order=OrderType.descending):
        if order is OrderType.ascending:
            return GoodsPost.query.limit(limit).offset(offset).all()
        return GoodsPost.query.order_by(db.desc(cls.id)).limit(limit).offset(offset).all()

    @classmethod
    def gets_by_student(cls, student_id, limit=10, offset=0, order=OrderType.descending):
        if order is OrderType.descending:
            return GoodsPost.query.order_by(db.desc(cls.id)).filter_by(
                student_id=student_id).limit(limit).offset(offset).all()
        return GoodsPost.query.filter_by(
            student_id=student_id).limit(limit).offset(offset).all()

    @classmethod
    def add(cls, student_id, switch, mobile, wechat, imgs, message):
        post = GoodsPost(student_id, switch, mobile, wechat, imgs, message)
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def defuzzy(cls, fuzzy_id):
        return decrypt(fuzzy_id)

    @property
    def fuzzy_id(self):
        return encrypt(str(self.id))

    @property
    def student(self):
        return Student.get(self.student_id)

    @property
    def status(self):
        return PostStatus(self.status_)

    @property
    def image_ids(self):
        return self.imgs.split(',') if self.imgs else []

    @property
    def images_urls(self):
        # TODO get urls
        return self.image_ids

    def _get_pv(self):
        key = self._post_pv_by_id_cache_key % self.id
        cached = int(rd.get(key)) if rd.get(key) else None
        if cached is not None:
            return cached
        rd.set(key, self.pv_)
        return self.pv_

    def _set_pv(self, pv_):
        rd.set(self._post_pv_by_id_cache_key % self.id, pv_)
        if pv_ % 7 == 0:
            self.pv_ = pv_
            db.session.add(self)
            db.session.commit()
            self.clear_cache()

    pv = property(_get_pv, _set_pv)

    def update_self(self, data):
        if not data:
            return True
        if not self.editable:
            raise CannotEditPostError()
        message = data.get('message')
        switch = data.get('switch')
        wechat = data.get('wechat')
        if message:
            self.message = message
        if switch is not None:
            self.switch = switch
        if wechat is not None:
            self.wechat = wechat
        self.update_time = datetime.now()
        self.editable -= 1
        db.session.add(self)
        db.session.commit()
        self.clear_cache()
        return True

    def update_status(self, status):
        if status is PostStatus.normal:
            self.to_normal()
        if status is PostStatus.succeed:
            self.to_succeed()
        if status is PostStatus.abandoned:
            self.to_abandoned()

    def to_normal(self):
        if self.status is not PostStatus.normal:
            self.status_ = PostStatus.normal.value
            self.update_time = datetime.now()
            db.session.add(self)
            db.session.commit()
            self.clear_cache()

    def to_succeed(self):
        if self.status is not PostStatus.succeed:
            self.status_ = PostStatus.succeed.value
            self.update_time = datetime.now()
            db.session.add(self)
            db.session.commit()
            self.clear_cache()
            self.clear_related_view_records()

    def to_abandoned(self):
        if self.status is not PostStatus.abandoned:
            self.status_ = PostStatus.abandoned.value
            self.update_time = datetime.now()
            db.session.add(self)
            db.session.commit()
            self.clear_cache()
            self.clear_related_view_records()

    def clear_related_view_records(self):
        ViewRecord.delete_records_by_post(self.id, PostType.goods_post)

    def clear_cache(self):
        mc.delete(self._goods_post_by_id_cache_key % self.id)
