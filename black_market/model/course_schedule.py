from black_market.ext import db


class CourseSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    day = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)

    def __init__(self, course_id, day, start, end):
        self.course_id = course_id
        self.day = day
        self.start = start
        self.end = end

    def __repr__(self):
        return '<CourseSchedule of Course%s>' % self.course_id
