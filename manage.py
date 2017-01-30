import json
import xlrd
from collections import namedtuple

from flask_script import Manager

from black_market.ext import db
from black_market.app import create_app
from black_market.models.models import (
    Course, CourseSchedule, User, Post, Demand, Supply, Comment)

app = create_app()
manager = Manager(app)


@manager.command
def init_database():
    with app.app_context():
        db.reflect()
        db.drop_all()
        db.create_all()
        courses, course_schedules = init_courses()
        for course in courses:
            db.session.add(course)
        for schedule in course_schedules:
            db.session.add(schedule)
        db.session.commit()


@manager.command
def init_test_database():
    init_database()
    with app.app_context():
        user1 = User('test_user1', '15612345678', 'user1@qq.com', 'password1', 2013)
        user2 = User('test_user2', '18812345678', 'user2@qq.com', 'password2', 2014)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        for i in range(0, 15):
            post = Post(i % 2 + 1, 1485335704 + 12 * i, 'I am post' + str(i))
            demand = Demand(i+1, i + 10)
            supply = Supply(i+1, i + 14)
            db.session.add(post)
            db.session.add(demand)
            db.session.add(supply)
        db.session.commit()

        # post1 = Post(1, 1485335704, 'I am wzh and I want A.')
        # post2 = Post(2, 1485337704, 'I am hsy and I want B.')
        # post1_demand = Demand(1, 12)
        # post1_supply = Supply(1, 16)
        # post2_demand = Demand(2, 16)
        # post2_supply = Supply(2, 12)
        # comment = Comment(2, 1, 'Hello, I wanna exchange my A for your B.', 1485337804)
        # db.session.add(post1)
        # db.session.add(post2)
        # db.session.add(post1_demand)
        # db.session.add(post1_supply)
        # db.session.add(post2_demand)
        # db.session.add(post2_supply)
        # db.session.add(comment)
        # db.session.commit()


def convert(raw_course):
    if '习题课' in raw_course.name:
        return
    classroom = [dict(building=raw_course.classroom1[0:2],
                      room=raw_course.classroom1[2:5])]
    if raw_course.classroom2:
        classroom.append(dict(building=raw_course.classroom2[0:2],
                              room=raw_course.classroom2[2:5]))
    schedule = []
    days = {1: 'mon', 2: 'tue', 3: 'wed', 4: 'thu', 5: 'fri', 6: 'sat', 7: 'sun'}
    for i in range(1, 8):
        s = getattr(raw_course, (days.get(i)))
        if s and '--' in s:
            print(raw_course.name, s)
            start = s[:int(len(s) / 2)].replace('-', '')
            end = s[int(len(s) / 2):].replace('-', '')
            schedule.append(dict(start=start, end=end, day=i))
    return dict(
        classroom=classroom,
        credit=int(raw_course.credit),
        id=int(raw_course.number),
        name=raw_course.name.replace(' ', ''),
        prerequisites=raw_course.prerequisites,
        schedule=schedule,
        teacher=raw_course.teacher,
        type=raw_course.type
    )


def init_courses():
    with open('courses.json', 'r') as f:
        courses_data = json.load(f)
    courses = []
    course_schedules = []
    for course_data in courses_data:
        id = course_data.get('id')
        name = course_data.get('name')
        credit = course_data.get('credit')
        teacher = course_data.get('teacher')
        course_type = course_data.get('type')
        schedule = course_data.get('schedule')
        classroom = course_data.get('classroom')
        pre = course_data.get('prerequisites')
        courses.append(Course(name, teacher, credit, course_type, classroom, pre))
        for s in schedule:
            course_schedules.append(CourseSchedule(
                id, s.get('day'), s.get('start'), s.get('end')))
    return courses, course_schedules


@manager.command
def generate_json():
    data = xlrd.open_workbook('course_schedules.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows

    RawCourse = namedtuple(
        'Course', ['number', 'name', 'type', 'prerequisites', 'credit',
                   'num_of_week', 'teacher', 'mon', 'tue', 'wed', 'thu',
                   'fri', 'sat', 'sun', 'classroom1', 'classroom2'])

    raw_courses = [RawCourse._make(table.row_values(i)) for i in range(1, nrows)]

    courses = []
    for rc in raw_courses:
        if convert(rc):
            courses.append(convert(rc))
    with open('courses.json', 'w') as f:
        f.write((json.dumps(courses)))


if __name__ == '__main__':
    manager.run()
