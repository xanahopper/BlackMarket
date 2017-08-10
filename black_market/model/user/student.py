from datetime import datetime

from black_market.ext import db
from black_market.model.wechat.user import WechatUser
from black_market.model.utils import validator
from black_market.model.user.consts import AccountStatus
from black_market.model.exceptions import MobileAlreadyExistedError
from black_market.model.exceptions import WechatUserNotFoundError


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('wechat_user.id'))
    name = db.Column(db.String(80))
    mobile = db.Column(db.String(80), primary_key=True, index=True)
    open_id = db.Column(db.String(80), db.ForeignKey('wechat_user.open_id'))
    type = db.Column(db.SmallInteger)
    grade = db.Column(db.String(10))
    status = db.Column(db.SmallInteger, default=AccountStatus.need_verify.value)
    create_time = db.Column(db.DateTime(), default=datetime.now())
    update_time = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())

    _cache_key_prefix = 'student:'
    _student_cache_key = _cache_key_prefix + 'id:%s'

    def __init__(self, id_, name, mobile, open_id, type_, grade, status):
        self.id = id_
        self.name = name if name else ''
        self.mobile = mobile
        self.open_id = open_id
        self.type = type_.value
        self.grade = grade
        self.status = status.value

    def __repr__(self):
        return '<User @%s>' % self.name

    def dump(self):
        return dict(
            id=self.id, username=self.username, mobile=self.mobile,
            grade=self.grade, type=self.type, status=self.status,
            create_time=self.create_time, update_time=self.update_time)

    @classmethod
    def add(cls, id_, name, mobile, open_id, type_, grade, status=AccountStatus.need_verify):
        wechat_user = WechatUser.get_by_open_id(open_id)
        if wechat_user is None:
            raise WechatUserNotFoundError()
        if Student.existed(mobile):
            raise MobileAlreadyExistedError
        student = Student(id_, name, mobile, open_id, type_, grade, status)
        db.session.add(student)
        db.session.commit()
        return student.id

    @classmethod
    def get(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def existed(cls, mobile):
        return bool(cls.query.filter_by(mobile=mobile).first())

    @property
    def wechat_user(self):
        return WechatUser.get_by_open_id(self.open_id)

    @property
    def username(self):
        return self.name if self.name else self.wechat_user.nickname

    @property
    def posts(self, limit=10, offset=0):
        from black_market.model.post.course import CoursePost
        return CoursePost.gets_by_student(self.id, limit, offset)

    def update(self, name, type_, grade):
        self.name = name.strip()
        self.type = type_.value
        self.grade = grade
        db.session.add(self)
        db.session.commit()
        return Student.get(self.id)

    def change_mobile(self, mobile):
        validator.validate_phone(mobile)
        if Student.existed(mobile):
            raise MobileAlreadyExistedError
        self.mobile = mobile
        db.session.add(self)
        db.session.commit()

    @property
    def account_status(self):
        return AccountStatus(self.status)

    def need_verify(self):
        return self.account_status is AccountStatus.need_verify

    def is_normal(self):
        return self.account_status is AccountStatus.normal

    def to_normal(self):
        self.status = AccountStatus.normal.value
        db.session.add(self)
        db.session.commit()
