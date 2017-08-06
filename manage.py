import sys
import runpy
import json
import xlrd
from collections import namedtuple


from oauthlib.common import generate_token
from flask_script import Manager
from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand

from black_market.ext import db
from black_market.app import create_app
from black_market.model.post.course import CoursePost
from black_market.model.post.course_demand import CourseDemand
from black_market.model.post.course_supply import CourseSupply

from black_market.model.user.account import Account
from black_market.model.user.student import Student
from black_market.model.user.alias import StudentAccountAlias
from black_market.model.user.consts import AccountType, StudentType, AccountStatus, Gender
from black_market.model.oauth.token import OAuthToken
from black_market.model.oauth.client import OAuthClient
from black_market.model.oauth.grant import OAuthGrant

from black_market.model.course import Course
from black_market.model.course_schedule import CourseSchedule

import flask_script

from black_market.config import DEBUG, HTTP_HOST, HTTP_PORT

app = create_app()
manager = Manager(app)
alchemydumps = AlchemyDumps(app, db)

manager.add_command(flask_script.commands.ShowUrls())
manager.add_command('alchemydumps', AlchemyDumpsCommand)


@manager.command
def init_database():
    with app.app_context():
        db.reflect()
        db.drop_all()
        db.create_all()

        print('Adding Client `Web`')
        id_ = OAuthClient.add('web', AccountType.student, allowed_scopes=['student'])
        client = OAuthClient.get(id_)
        print('Client ID: %s' % client.client_id)

        print('\nAdding Student @mew_wzh')
        id_ = Student.add(
            'mew_wzh', Gender.male, '2014',StudentType.double_major,
            '19950629', '15600000000', AccountStatus.need_verify)
        student = Student.get(id_)
        print(student.dump())

        print('\nAdding token for user @mew_wzh')
        id_ = OAuthToken.add(client.id, id_, ['student'], generate_token(), generate_token())
        token = OAuthToken.get(id_)
        print(token.dump())

        courses, course_schedules = _init_courses()
        for course in courses:
            db.session.add(course)
        for schedule in course_schedules:
            db.session.add(schedule)
        db.session.commit()


@manager.command
def test():
    with app.app_context():
        # c1 = Class.query.first()
        # print(c1.students)
        # print(c1.students.all())

        # s1 = Student.query.first()
        #
        # print(11111, s1._class)
        #
        # rs = s1._class.all()
        #
        # for r in rs:
        #     print(2222, r._class, r.student)
        pass


@manager.command
def init_test_database():
    init_database()
    with app.app_context():
        user1 = User(
            'test_user1', '15612345671', 'user1@qq.com', 'password1', 2013)
        user2 = User(
            'test_user2', '15612345672', 'user2@qq.com', 'password2', 2014)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        for i in range(0, 15):
            post = Post(
                i % 2 + 1, 1486200246 + 1800 * i, '1561234567%d' % (i % 2 + 1),
                '我是xxx，跪求xxx课，请联系我！')
            # demand = Demand(i + 1, i + 10)
            # supply = Supply(i + 1, i + 14)
            db.session.add(post)
            # db.session.add(demand)
            # db.session.add(supply)
        db.session.commit()


def convert(raw_course):
    if '习题课' in raw_course.name:
        return
    classroom = [dict(building=raw_course.classroom1[0:2],
                      room=raw_course.classroom1[2:5])]
    if raw_course.classroom2:
        classroom.append(dict(building=raw_course.classroom2[0:2],
                              room=raw_course.classroom2[2:5]))
    schedule = []
    days = {1: 'mon', 2: 'tue',
            3: 'wed', 4: 'thu',
            5: 'fri', 6: 'sat',
            7: 'sun'}
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


def _init_courses():
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
        courses.append(
            Course(name, teacher, credit))
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

    raw_courses = [
        RawCourse._make(table.row_values(i)) for i in range(1, nrows)]

    courses = []
    for rc in raw_courses:
        if convert(rc):
            courses.append(convert(rc))
    with open('courses.json', 'w') as f:
        f.write((json.dumps(courses)))


def _make_shell_context():
    return dict(app=app, db=db, **locals())


@manager.command
def shell():
    """IPython shell"""
    from IPython.terminal.ipapp import TerminalIPythonApp
    app = TerminalIPythonApp.instance()
    app.user_ns = _make_shell_context()
    app.display_banner = False
    app.initialize(argv=[])
    app.start()


# TODO redis
# @manager.command
# def cleanup_redis():
#     """Flush all redis cache."""
#     if not DEBUG:
#         raise Exception('Redis cleanup is not allowed in non-debug environ.')
#
#     mc.flushall()


@manager.option(dest='args', nargs='*', help='-- args for script')
def rebuild_sql(args):
    """Run test.memdb with options, eg: ./manage.py rebuild_sql -- -i"""
    if not DEBUG:
        raise Exception('Sql rebuild is not allowed in non-debug environ.')

    script_mod = 'tests.memdb'
    sys.argv = ['-d database/'] + args
    runpy.run_module(script_mod, run_name='__main__', alter_sys=True)


@manager.command
def runserver(host=None, port=None, debug=None):
    """Run a flask development server"""
    app.run(
        host=host or HTTP_HOST or '0.0.0.0',
        port=port or HTTP_PORT or '9000',
        debug=DEBUG,
        use_debugger=True,
        use_reloader=DEBUG,
    )


@manager.command
def gunicorn(workers=4, timeout=60):
    """Serve with gunicorn"""
    from gunicorn.app.base import Application

    host = HTTP_HOST or '0.0.0.0'
    port = HTTP_PORT or '9000'
    bind = '{0}:{1}'.format(host, port)

    class MyApp(Application):
        def init(self, parser, opts, args):
            return {
                'bind': bind,
                'timeout': timeout,
                'workers': workers,
                'worker_class': 'gevent'
            }

        def load(self):
            return app

    MyApp().run()


if __name__ == '__main__':
    manager.run()
