from black_market.ext import db, login_manager


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    teacher = db.Column(db.String(80))
    credit = db.Column(db.Integer)
    schedules = db.relationship('CourseSchedule', backref='course',
                                lazy='dynamic')

    def __init__(self, name, teacher, credit, course_type, classroom, pre):
        self.name = name
        self.teacher = teacher
        self.credit = credit
        self.course_type = course_type
        self.classroom = classroom
        self.prerequisites = pre

    def __repr__(self):
        return '<Course %s>' % self.name


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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    grade = db.Column(db.String(56))
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __init__(self, name, phone, email, password, grade):
        self.name = name
        self.phonee = phone
        self.email = email
        self.password = password
        self.grade = grade

    def __repr__(self):
        return '<User %s>' % self.name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer)
    created_time = db.Column(db.Integer)
    message = db.Column(db.String(256))
    demand = db.relationship('Demand', backref='post', lazy='dynamic')
    supply = db.relationship('Supply', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, user_id, created_time, message, status=0):
        self.user_id = user_id
        self.created_time = created_time
        self.message = message
        self.status = status

    def __repr__(self):
        return '<Post of %s at %s>' % (self.user_id, self.created_time)


class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __init__(self, post_id, course_id):
        self.post_id = post_id
        self.course_id = course_id

    def __repr__(self):
        return '<Demand for course %s of post %s>' % (
            self.course_id, self.post_id)


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __init__(self, post_id, course_id):
        self.post_id = post_id
        self.course_id = course_id

    def __repr__(self):
        return '<Supply for course %s of post %s>' % (
            self.course_id, self.post_id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(256))
    created_time = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, user_id, post_id, content, created_time, status=1):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.status = status
        self.created_time = created_time

    def __repr__(self):
        return '<Comment on %s at %s>' % (self.post_id, self.created_time)
