from black_market.ext import db
from black_market.model.const import CourseType


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    teacher = db.Column(db.String(80))
    credit = db.Column(db.Integer)
    schedules = db.relationship('CourseSchedule', backref='course',
                                lazy='dynamic')

    def __init__(self, name, teacher, credit):
        self.name = name
        self.teacher = teacher
        self.credit = credit

    def __repr__(self):
        return '<%s-%s-%s>' % (self.id, self.name, self.teacher)

    def dump(self):
        return dict(id=self.id, name=self.name, teacher=self.teacher, credit=self.credit)

    @property
    def type_(self):
        return CourseType(self.course_type)

    @classmethod
    def get(cls, id_):
        return Course.query.get(id_)

    @classmethod
    def gets(cls, limit=5, offset=0):
        return Course.query.limit(limit).offset(offset).all()

    @classmethod
    def get_by_name(cls, name):
        return Course.query.filter(Course.name.ilike('%' + name + '%'))
