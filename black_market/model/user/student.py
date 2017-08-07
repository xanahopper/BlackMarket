from datetime import datetime

from black_market.ext import db
from black_market.model.wechat.user import WechatUser
from black_market.model.utils import validator
from black_market.model.user.consts import AccountStatus
from black_market.model.exceptions import MobileAlreadyExistedError
from black_market.model.exceptions import WechatUserNotExistedError


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('wechat_user_info.id'))
    name = db.Column(db.String(80))
    mobile = db.Column(db.String(80), primary_key=True, index=True)
    open_id = db.Column(db.String(80), db.ForeignKey('wechat_user_info.open_id'))
    type = db.Column(db.SmallInteger)
    grade = db.Column(db.String(10))
    status = db.Column(db.SmallInteger, default=AccountStatus.need_verify.value)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    _cache_key_prefix = 'student:'
    _student_cache_key = _cache_key_prefix + 'id:%s'

    def __init__(self, name, mobile, open_id, type_, grade, status):
        self.name = name
        self.mobile = mobile
        self.open_id = open_id
        self.type = type_
        self.grade = grade
        self.status = status.value

    def __repr__(self):
        return '<User @%s>' % self.name

    def dump(self):
        return dict(id=self.id, name=self.name, gender=self.gender,
                    grade=self.grade, type=self.type, status=self.status)

    @classmethod
    def add(cls, mobile, open_id, type_, grade, status=AccountStatus.need_verify):
        wechat_user = WechatUser.get_by_open_id(open_id)
        if wechat_user is None:
            raise WechatUserNotExistedError
        if Student.existed(mobile):
            raise MobileAlreadyExistedError

        student = Student(mobile, open_id, type_, grade, status)

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def existed(cls, mobile):
        return bool(cls.query.filter_by(mobile=mobile).first())

    @property
    def posts(self, offset=0, limit=10):
        from black_market.model.post.course import CoursePost
        return CoursePost.gets_by_student(self.id, offset, limit)

    def change_mobile(self, mobile):
        validator.validate_phone(mobile)
        if StudentAccountAlias.existed(mobile, AliasType.mobile):
            raise MobileAlreadyExistedError
        self.update_alias(mobile, AliasType.mobile)

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
