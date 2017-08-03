from datetime import datetime

from black_market.ext import db
from black_market.model.utils import validator
from black_market.model.user.password import gen_salt, hash_password
from black_market.model.user.account import Account
from black_market.model.user.alias import AliasBase, StudentAccountAlias
from black_market.model.user.consts import AliasType, AccountStatus, AccountType, Gender
from black_market.model.exceptions import (
    MobileAlreadyExistedError, EmailAlreadyExistedError,
    WeixinAlreadyExistedError, AliasAlreadyExistedError
)


class Student(AliasBase, db.Model):
    __tablename__ = 'student'
    _alias_cls = StudentAccountAlias

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    gender = db.Column(db.SmallInteger, default=Gender.unknown.value)
    type = db.Column(db.SmallInteger)
    grade = db.Column(db.String(10))
    password = db.Column(db.String(80))
    salt = db.Column(db.String(80))
    status = db.Column(db.SmallInteger, default=AccountStatus.need_verify.value)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    account_type = AccountType.student

    _cache_key_prefix = 'student:'
    _student_cache_key = _cache_key_prefix + 'id:%s'

    def __init__(self, id, name, gender, grade, type, password, salt, status):
        self.id = id
        self.name = name
        self.gender = gender
        self.grade = grade
        self.type = type
        self.password = password
        self.status = status.value
        self.salt = salt

    def __repr__(self):
        return '<User @%s>' % self.name

    # def ping(self):
    #     self.last_seen = datetime.now()
    #     db.session.add(self)
    #     db.session.commit()

    @classmethod
    def add(cls, name, gender, grade, type_, raw_password, mobile, status, alias_type=AliasType.mobile):

        if StudentAccountAlias.existed(mobile, alias_type):
            if alias_type is AliasType.mobile:
                raise MobileAlreadyExistedError
            if alias_type is AliasType.email:
                raise EmailAlreadyExistedError
            if alias_type is AliasType.weixin:
                raise WeixinAlreadyExistedError
            else:
                raise AliasAlreadyExistedError

        id_ = Account.add(cls.account_type)
        salt = gen_salt()
        password = hash_password(raw_password, salt)
        student = Student(id_, name, gender.value, grade, type_.value, password, salt, status)
        db.session.add(student)
        db.session.commit()
        StudentAccountAlias.add(id_, mobile, alias_type)

        return id_

    def dump(self):
        return dict(id=self.id, name=self.name, gender=self.gender,
                    grade=self.grade, type=self.type, status=self.status)

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @property
    def alias(self):
        return self._alias_cls.query.filter_by(id=self.id, type=AliasType.mobile.value)

    def change_mobile(self, mobile):
        validator.validate_phone(mobile)
        if StudentAccountAlias.existed(mobile, AliasType.mobile):
            raise MobileAlreadyExistedError
        self.update_alias(mobile, AliasType.mobile)

    def update_alias(self, mobile, alias_type):
        StudentAccountAlias.update_alias(self.id, mobile, alias_type)

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

    def verify_password(self, raw_password):
        return self.password == hash_password(raw_password, self.salt)

    def change_password(self, new_password):
        # from black_market.model.oauth.token import delete_oauth_tokens
        salt = gen_salt()
        validator.validate_password(new_password)
        password = hash_password(new_password, salt)
        self.salt = salt
        self.password = password
        db.session.add(self)
        db.session.commit()

        # TODO
        # delete_oauth_tokens(self.id_)
