import json
from datetime import datetime

from black_market.ext import db
from black_market.model.user.consts import UserBehaviorType


class UserBehavior(db.Model):
    __tablename__ = 'user_behavior'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(80))
    type_ = db.Column(db.SmallInteger)
    detail = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, type_, detail):
        self.user_id = user_id
        self.type_ = type_.value
        self.detail = detail

    def __repr__(self):
        return '<UserBehavior:user%s:%s>' % (self.user_id, self.behavior_name)

    def dump(self):
        return dict(id=self.id, type=self.type_, detail=self.detail)

    @property
    def behavior_type(self):
        return UserBehaviorType(self.type_)

    @property
    def behavior_name(self):
        return self.behavior_type.name

    @classmethod
    def add(cls, user_id, type_, detail):
        detail = json.dumps(detail)
        behavior = UserBehavior(user_id, type_, detail)
        db.session.add(behavior)
        db.session.commit()

    @classmethod
    def get(cls, id_):
        return cls.query.filter_by(id=id_).first()
