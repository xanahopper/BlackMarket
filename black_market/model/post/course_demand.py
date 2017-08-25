import pickle

from black_market.ext import db
from black_market.libs.cache.redis import mc, ONE_DAY
from black_market.model.course import Course


class CourseDemand(db.Model):
    __tablename__ = 'course_demand'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('course_post.id'))
    course_id = db.Column(db.Integer)

    _cache_key_prefix = 'course:post:demand:'
    _course_post_demand_by_id_cache_key = _cache_key_prefix + 'id:%s'

    def __init__(self, post_id, course_id):
        self.post_id = post_id
        self.course_id = course_id

    def dump(self):
        return dict(id=self.id, post_id=self.post_id, course=self.course.dump())

    def share_dump(self):
        return dict(course=self.course.dump())

    @classmethod
    def add(cls, post_id, course_id):
        demand = CourseDemand(post_id, course_id)
        db.session.add(demand)
        db.session.commit()
        return demand.id

    @classmethod
    def get(cls, id_):
        cache_key = cls._course_post_demand_by_id_cache_key % id_
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        course_demand = CourseDemand.query.get(id_)
        if course_demand:
            mc.set(cache_key, pickle.dumps(course_demand).hex())
            mc.expire(cache_key, ONE_DAY)
        return course_demand

    @classmethod
    def get_by_post(cls, id_):
        return CourseDemand.query.filter_by(post_id=id_).first()

    @classmethod
    def get_by_course(cls, id_):
        return CourseDemand.query.filter_by(course_id=id_).all()

    @property
    def post(self):
        from black_market.model.post.course import CoursePost
        return CoursePost.get(self.post_id)

    @property
    def course(self):
        return Course.get(self.course_id)

    @property
    def course_name(self):
        return self.course.name

    @property
    def course_teacher(self):
        return self.course.teacher

    def clear_cache(self):
        mc.delete(self._course_post_demand_by_id_cache_key % self.id)

    def delete(self):
        self.clear_cache()
        db.session.delete(self)
        db.session.commit()
