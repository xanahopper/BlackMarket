from datetime import datetime

from black_market.ext import db
from black_market.libs.cache.redis import rd
from black_market.model.user.student import Student
from black_market.model.post.consts import PostStatus
from black_market.model.exceptions import SupplySameAsDemandError, InvalidPostError


class GoodsPost(db.Model):
    __tablename__ = 'goods_post'

    _cache_key_prefix = 'goods:post:'
    _post_pv_cache_key = _cache_key_prefix + '%s:pv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    status_ = db.Column(db.SmallInteger)
    switch = db.Column(db.SmallInteger)
    mobile = db.Column(db.String(80))
    wechat = db.Column(db.String(80))
    message = db.Column(db.String(256))
    pv_ = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime(), default=datetime.now())
    update_time = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, student_id, switch, mobile, wechat, message, status=PostStatus.normal):
        self.student_id = student_id
        self.switch = switch.value
        self.mobile = mobile
        self.wechat = wechat
        self.message = message
        self.status_ = status.value

    def __repr__(self):
        return '<CoursePost of %s at %s>' % (self.student_id, self.created_time)

    def dump(self):
        return dict(id=self.id, student_id=self.student_id, student_name=self.student.name,
                    supply=self.supply.dump(), demand=self.demand.dump(),
                    mobile=self.mobile, wechat=self.wechat, message=self.message, pv=self.pv,
                    create_time=self.create_time, update_time=self.update_time)

    @classmethod
    def get(cls, id_):
        return GoodsPost.query.get(id_)

    @classmethod
    def gets(cls, limit=5, offset=0):
        return GoodsPost.query.limit(limit).offset(offset).all()

    @classmethod
    def gets_by_student(cls, student_id, limit=10, offset=0):
        return GoodsPost.query.filter_by(student_id=student_id).limit(limit).offset(offset).all()

    @classmethod
    def add(cls, student_id, switch, mobile, wechat, message):
        post = GoodsPost(student_id, switch, mobile, wechat, message)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def validate_supply_and_demand(supply_course_id, demand_course_id):
        if supply_course_id == demand_course_id:
            raise SupplySameAsDemandError()

        if supply_course_id == 30 and demand_course_id == 31:
            raise InvalidPostError()

    @property
    def student(self):
        return Student.get(self.student_id)

    @property
    def status(self):
        return PostStatus(self.status_)

    def _get_pv(self):
        key = self._post_pv_cache_key % self.id_
        cached = rd.get(key)
        if cached is not None:
            return cached
        rd.set(key, self.pv_)
        return self.pv_

    def _set_pv(self, pv_):
        rd.set(self._post_pv_cache_key % self.id_, pv_)
        if pv_ % 7 == 0:
            self.pv_ = pv_
            db.session.add(self)
            db.session.commit()

    pv = property(_get_pv, _set_pv)

    def update_self(self, data):
        if not data:
            return True
        status = data.get('status')
        message = data.get('message')
        if status:
            self.status_ = status
        if message:
            self.message = message
        self.update_time = datetime.now()
        db.session.add(self)
        db.session.commit()
        return True

    def to_normal(self):
        if self.status is not PostStatus.normal:
            self.update_self(dict(status=PostStatus.normal.value))

    def to_succeed(self):
        if self.status is not PostStatus.succeed:
            self.update_self(dict(status=PostStatus.succeed.value))

    def to_abandoned(self):
        if self.status is not PostStatus.abandoned:
            self.update_self(dict(status=PostStatus.abandoned.value))

    def update_supply(self, supply_course_id):
        supply = self.supply
        demand = self.demand
        self.validate_supply_and_demand(supply_course_id, demand.course_id)
        supply.course_id = supply_course_id
        self.update_time = datetime.now()
        db.session.add(supply)
        db.session.add(self)
        db.session.commit()

    def update_demand(self, demand_course_id):
        supply = self.supply
        demand = self.demand
        self.validate_supply_and_demand(supply.course_id, demand_course_id)
        demand.course_id = demand_course_id
        self.update_time = datetime.now()
        db.session.add(demand)
        db.session.add(self)
        db.session.commit()
