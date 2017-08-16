import pickle

from black_market.ext import db
from black_market.libs.cache.redis import mc, ONE_DAY
from black_market.model.course_schedule import CourseSchedule
from black_market.model.const import CourseType


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    teacher = db.Column(db.String(80))
    credit = db.Column(db.Integer)

    _cache_key_prefix = 'course:'
    _course_cache_key = _cache_key_prefix + 'id:%s'
    _all_course_cache_key = _cache_key_prefix + 'all'

    def __init__(self, name, teacher, credit, type_):
        self.name = name
        self.teacher = teacher
        self.credit = credit
        self.type_ = type_

    def dump(self):
        return dict(id=self.id, name=self.name, teacher=self.teacher, credit=self.credit,
                    schedules=[s.dump() for s in self.schedules])

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
        cache_key = cls._course_cache_key % id_
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        else:
            course = Course.query.get(id_)
            if course:
                mc.set(cache_key, pickle.dumps(course).hex())
                mc.expire(cache_key, ONE_DAY)
            return course

    @classmethod
    def gets(cls, limit=5, offset=0):
        return Course.query.limit(limit).offset(offset).all()

    @classmethod
    def get_all(cls):
        cache_key = cls._all_course_cache_key
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        else:
            courses = Course.query.all()
            mc.set(cache_key, pickle.dumps(courses).hex())
            mc.expire(cache_key, ONE_DAY)
            return courses

    @classmethod
    def get_by_name(cls, name):
        return Course.query.filter(Course.name.ilike('%' + name + '%'))

    @property
    def type(self):
        return CourseType(self.type_)

    @property
    def schedules(self):
        return CourseSchedule.get_by_course(self.id)

    def clear_cache(self):
        mc.delete(self._course_cache_key % self.id)
