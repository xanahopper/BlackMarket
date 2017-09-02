import sys
import runpy
import json
import xlrd
import flask_script
from collections import namedtuple

from flask_script import Manager
from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand

from black_market.ext import db
from black_market.libs.cache.redis import mc, rd
from black_market.app import create_app
from black_market.config import DEBUG, HTTP_HOST, HTTP_PORT

from black_market.model.wechat.user import WechatUser
from black_market.model.wechat.session import WechatSession
from black_market.model.user.student import Student
from black_market.model.user.behavior import UserBehavior
from black_market.model.user.view_record import ViewRecord
from black_market.model.user.consts import StudentType, AccountStatus, Gender

from black_market.model.course import Course
from black_market.model.course_schedule import CourseSchedule
from black_market.model.post.course import CoursePost
from black_market.model.post.course_demand import CourseDemand
from black_market.model.post.course_supply import CourseSupply
from black_market.model.post.goods import GoodsPost
from black_market.model.file.photo import FilePhoto

app = create_app()
manager = Manager(app)
alchemydumps = AlchemyDumps(app, db)

manager.add_command(flask_script.commands.ShowUrls())
manager.add_command('alchemydumps', AlchemyDumpsCommand)


@manager.command
def init_database():

    if not DEBUG:
        print('NOT DEBUG MODE!!!')
        return

    with app.app_context():
        db.engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        db.reflect()
        db.drop_all()
        db.create_all()

        courses, course_schedules = _init_courses()
        for course in courses:
            db.session.add(course)
        for course_schedule in course_schedules:
            db.session.add(course_schedule)
        db.session.commit()

        mc.flushdb()
        rd.flushdb()


def convert(raw_course):
    if '习题课' in raw_course.name:
        return
    classroom = [dict(building=raw_course.classroom[0:2],
                      room=raw_course.classroom[2:5])]
    schedule = []
    days = {1: 'mon', 2: 'tue',
            3: 'wed', 4: 'thu',
            5: 'fri', 6: 'sat',
            7: 'sun'}
    for i in range(1, 8):
        s = getattr(raw_course, (days.get(i)))
        if s and '--' in s:
            # print(raw_course.name, s)
            frequency = 'every'
            if '（单周）' in s:
                frequency = 'odd'
                s = s.rstrip('（单周）')
            elif '（双周）' in s:
                frequency = 'even'
                s = s.rstrip('（双周）')
            print(raw_course.name, s)
            start = s[:int(len(s) / 2)].replace('-', '')
            end = s[int(len(s) / 2):].replace('-', '')
            schedule.append(dict(start=start, end=end, day=i, frequency=frequency))
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
            Course(name, teacher, credit, course_type))
        for s in schedule:
            course_schedules.append(CourseSchedule(
                id, s.get('day'), s.get('start'), s.get('end'), s.get('frequency')))
    return courses, course_schedules


@manager.command
def generate_json():
    data = xlrd.open_workbook('course_schedules.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows

    RawCourse = namedtuple(
        'Course', ['number', 'name', 'type', 'prerequisites', 'credit',
                   'num_of_week', 'teacher', 'mon', 'tue', 'wed', 'thu',
                   'fri', 'sat', 'sun', 'classroom'])

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
def gunicorn(host=None, port=5000, workers=4, timeout=60):
    """Serve with gunicorn"""
    from gunicorn.app.base import Application

    host = host or HTTP_HOST or '127.0.0.1'
    port = port or HTTP_PORT or '5000'
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
