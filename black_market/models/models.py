from black_market.ext import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    teacher = db.Column(db.String(80))
    credit = db.Column(db.String(80))

    def __init__(self, name, teacher, credit):
        self.name = name
        self.teacher = teacher
        self.credit = credit

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
    name = db.Column(db.String(80), unique=True)
    tel = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    grade = db.Column(db.String(4))
    avatar_url = db.Column(db.String(128))

    def __init__(self, name, tel, email, password, grade, avatar_url=None):
        self.name = name
        self.tel = tel
        self.email = email
        self.password = password
        self.grade = grade
        self.avatar_url = avatar_url

    def __repr__(self):
        return '<User %s>' % self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    demand_id = db.Column(db.Integer, db.ForeignKey('demand.id'))
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    status = db.Column(db.Integer)
    created_time = db.Column(db.Integer)
    content = db.Column(db.String(256))

    def __init__(self, user_id, demand_id, supply_id,
                 created_time, content, status):
        self.user_id = user_id
        self.demand_id = demand_id
        self.supply_id = supply_id
        self.created_time = created_time
        self.content = content
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

    def __init__(self, user_id, post_id, content, created_time, status):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.status = status

    def __repr__(self):
        return '<Comment on %s at %s>' % (self.post_id, self.created_time)
