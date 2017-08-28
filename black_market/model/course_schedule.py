from black_market.ext import db


class CourseSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    day = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    frequency = db.Column(db.String(10))

    def __init__(self, course_id, day, start, end, frequency):
        self.course_id = course_id
        self.day = day
        self.start = start
        self.end = end
        self.frequency = frequency

    def dump(self):
        return dict(id=self.id, course_id=self.course_id,
                    day=self.day, start=self.start, end=self.end,
                    frequency=self.frequency)

    @classmethod
    def add(cls, course_id, day, start, end, frequency):
        schedule = CourseSchedule(course_id, day, start, end, frequency)
        db.session.add(schedule)
        db.session.commit()

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_course(cls, course_id):
        return cls.query.filter_by(course_id=course_id).all()
