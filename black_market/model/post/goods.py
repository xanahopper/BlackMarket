from datetime import datetime

from black_market.ext import db
from black_market.model.user.student import Student
from black_market.model.post.consts import PostStatus


class GoodsPost(db.Model):
    __tablename__ = 'goods_post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    status_ = db.Column(db.SmallInteger)
    contact = db.Column(db.String(80))
    message = db.Column(db.String(256))
    create_time = db.Column(db.DateTime(), default=datetime.utcnow())
    update_time = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, student_id, contact, message, status=PostStatus.normal):
        self.student_id = student_id
        self.contact = contact
        self.message = message
        self.status_ = status.value

    def __repr__(self):
        return '<GoodsPost of %s at %s>' % (self.student_id, self.created_time)

    def dump(self):
        return dict(id=self.id, student_id=self.student_id, student_name=self.student.name,
                    contact=self.contact, message=self.message, create_time=self.create_time,
                    update_time=self.update_time)

    @classmethod
    def add(cls, student_id, contact, message):
        post = GoodsPost(student_id, contact, message)
        db.session.add(post)
        db.session.commit()

    @classmethod
    def get(cls, id_):
        return GoodsPost.query.get(id_)

    @classmethod
    def gets(cls, limit=5, offset=0):
        return GoodsPost.query.limit(limit).offset(offset).all()

    @classmethod
    def gets_by_student(cls, student_id, limit=10, offset=0):
        return GoodsPost.query.filter_by(student_id=student_id).limit(limit).offset(offset).all()

    @property
    def student(self):
        return Student.get(self.student_id)

    @property
    def status(self):
        return PostStatus(self.status_)

    def update_self(self, data):
        if not data:
            return True
        status = data.get('status')
        contact = data.get('contact')
        message = data.get('message')
        if status:
            self.status_ = status
        if contact:
            self.contact = contact
        if message:
            self.message = message
        self.update_time = datetime.utcnow()
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
