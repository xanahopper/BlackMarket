from black_market.ext import db
from black_market.model.course import Course


class CourseSupply(db.Model):
    __tablename__ = 'course_supply'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('course_post.id'))
    course_id = db.Column(db.Integer)

    def __init__(self, post_id, course_id):
        self.post_id = post_id
        self.course_id = course_id

    def __repr__(self):
        return '<CourseSupply of Post %s>' % (self.post_id)

    def dump(self):
        return dict(id=self.id, post_id=self.post_id, course_id=self.course.id)

    @classmethod
    def get(cls, id_):
        return CourseSupply.query.get(id_)

    @classmethod
    def get_by_post(cls, id_):
        return CourseSupply.query.filter_by(post_id=id_).first()

    @classmethod
    def get_by_course(cls, id_):
        return CourseSupply.query.filter_by(course_id=id_).all()

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
