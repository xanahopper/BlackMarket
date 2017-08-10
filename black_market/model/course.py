from black_market.ext import db
from black_market.model.course_schedule import CourseSchedule
from black_market.model.const import CourseType


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    teacher = db.Column(db.String(80))
    credit = db.Column(db.Integer)

    def __init__(self, name, teacher, credit, type_):
        self.name = name
        self.teacher = teacher
        self.credit = credit
        self.type_ = type_

    def __repr__(self):
        return '<%s-%s-%s>' % (self.id, self.name, self.teacher)

    def dump(self):
        return dict(id=self.id, name=self.name, teacher=self.teacher, credit=self.credit,
                    schedule=[s.dump() for s in self.schedule])

    @classmethod
    def add(cls, name, teacher, credit, type_, schedules):
        course = Course(name, teacher, credit, type_.value)
        db.session.add(course)
        db.session.commit()
        for s in schedules:
            schedule = CourseSchedule(
                course.id, s['day'], s['start'], s['end'])
            db.session.add(schedule)
        db.session.commit()

    @classmethod
    def get(cls, id_):
        return Course.query.get(id_)

    @classmethod
    def gets(cls, limit=5, offset=0):
        return Course.query.limit(limit).offset(offset).all()

    @classmethod
    def get_by_name(cls, name):
        return Course.query.filter(Course.name.ilike('%' + name + '%'))

    @property
    def type(self):
        return CourseType(self.type_)

    @property
    def schedules(self):
        return CourseSchedule.get_by_course(self.id)
