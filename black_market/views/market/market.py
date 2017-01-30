import re
import datetime
import hashlib

from flask import Blueprint, flash, request, render_template, redirect, get_flashed_messages
from flask_login import login_user, logout_user, current_user, login_required

from black_market.ext import db
from black_market.libs.api import course as course_api
from black_market.models.models import Post, Supply, Demand, User

bp = Blueprint('market', __name__)


def timestamp_to_datetime(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime("%Y-%m-%d %H:%M:%S")


def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)


def check_phone(phone):
    pattern = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    return bool(pattern.match(phone))


def check_email(email):
    pattern = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")
    return bool(pattern.match(email))


def check_exist(phone):
    return bool(User.query.filter_by(tel=phone).first())

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register_page(msg=''):
    for m in get_flashed_messages(with_categories=False, category_filter=['reg']):
        msg = msg + m
    return render_template('register.html', msg=msg)


@bp.route('/verify', methods=['POST'])
def verify():
    # if info is wrong, back to /register
    # else make a post to get the msg
    # post to /reg (write into database)
    # g = xxx
    return render_template()


@bp.route('/reg', methods=['POST'])
def reg():
    # get data from g and g = None
    # get phone number
    # get username
    # get password
    # get grade
    # get email
    # go to posts
    phone = request.values.get('phone').strip()
    username = request.values.get('username').strip()
    raw_password = request.values.get('password').strip()
    grade = request.values.get('grade').strip()
    email = request.values.get('email').strip()

    if not check_phone(phone):
        return redirect_with_msg(
            '/register', u'Wrong phone number!', category='reg')
    if check_exist(phone):
        return redirect_with_msg(
            '/register', u'This phone number has been registered!', category='reg')
    if check_email(email) == '':
        return redirect_with_msg(
            '/register', u'Wrong email address!', category='reg')
    if username == '':
        return redirect_with_msg(
            '/register', u'Empty username is not allowed', category='reg')
    if raw_password == '':
        return redirect_with_msg(
            '/register',u'Empty password is not allowed',category='reg')
    m = hashlib.md5()
    m.update(raw_password.encode('utf-8'))
    password = m.hexdigest()
    user = User(username, phone, email, password, grade)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect('/posts')


@bp.route('/loginpage', methods=['GET', 'POST'])
def loginpage(msg=''):
    if current_user.is_authenticated:
        return redirect('/posts')
    for m in get_flashed_messages(with_categories=False, category_filter=['login']):
        msg = msg + m
    return render_template('loginpage.html', msg=msg)


@bp.route('/login')
def login():
    # check tel & password
    return redirect('/posts')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@bp.route('/posts', methods=['GET'])
def get_posts():
    return redirect('/posts/1')


@bp.route('/newpost', methods=['GET'])
def newpost_page():
    return render_template('newpost.html')


@bp.route('/post', methods=['POST'])
def post():
    return


def get_all_courses():
    courses = course_api.get_all_courses()
    s = ''
    for course in courses:
        s = s + str(course.id) + '.\t' + course.name + '<br>'
    return s


@bp.route('/course/<int:id>', methods=['GET'])
def get_course(id=None):
    course = course_api.get_course_by_id(id)
    if not course:
        return 'NULL'
    return str(id) + '. ' + course.name


@bp.route('/course/search', methods=['GET'])
def search_course():
    name = request.values.get('name')
    credit = request.values.get('credit')
    days = request.values.get('days')
    courses = course_api.search_course_by_filters(name, days, credit)
    s = ''
    if courses:
        for course in courses:
            s = s + str(course.id) + '.\t' + course.name + '<br>'
    return s


@bp.route('/posts/<int:page>', methods=['GET'])
def post_paginate(page, per_page=6):
    if not current_user.is_authenticated:

        print(current_user.is_authenticated)
        return redirect('/loginpage')
    paginate = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = []
    for post in paginate.items:
        time = timestamp_to_datetime(post.created_time)
        supply_course_id = Supply.query.filter_by(post_id=post.id).first().course_id
        demand_course_id = Demand.query.filter_by(post_id=post.id).first().course_id
        supply = dict(
            course_id=supply_course_id,
            course_name=course_api.get_course_by_id(supply_course_id).name)
        demand = dict(
            course_id=demand_course_id,
            course_name=course_api.get_course_by_id(demand_course_id).name)
        p = dict(time=time, supply=supply, demand=demand, message=post.message)
        posts.append(p)
    return render_template('posts.html', posts=posts, has_next=paginate.has_next, page=page)
