import time
import hashlib

from flask import (
    Blueprint, request, render_template,
    redirect, get_flashed_messages)
from flask_login import (
    login_user, logout_user, current_user)

from black_market.ext import db
from black_market.libs.api import course as course_api
from black_market.models.models import (
    Post, Supply, Demand, User, CourseSchedule)
from black_market.views.utils import (
    timestamp_to_datetime, redirect_with_msg, check_phone,
    check_email, check_exist, get_paginate_from_list,
    num_to_word, get_phone_words, get_short_message)

bp = Blueprint('market', __name__)


@bp.route('/', methods=['GET', 'POST'])
def search(per_page=6):
    page = request.values.get('page') or 1
    page = int(page)
    target_supply_text = request.values.get('supply') or ''
    target_demand_text = request.values.get('demand') or ''
    target_ss = course_api.search_course(target_supply_text)
    target_ds = course_api.search_course(target_demand_text)
    target_supply_ids = [c.id for c in target_ss] if target_ss else []
    target_demand_ids = [c.id for c in target_ds] if target_ds else []
    all_posts = [p for p in Post.query.order_by(Post.id.desc()).all()]
    target_posts = []
    for post in all_posts:
        supply_course_id = Supply.query.filter_by(
            post_id=post.id).first().course_id
        if target_ss is not None:
            if supply_course_id not in target_supply_ids:
                continue
        demand_course_id = Demand.query.filter_by(
            post_id=post.id).first().course_id
        if target_ds is not None:
            if demand_course_id not in target_demand_ids:
                continue
        target_posts.append(post)
    paginate, has_next = get_paginate_from_list(target_posts, page, per_page)
    posts = []
    for post in paginate:
        time = timestamp_to_datetime(post.created_time)
        supply_course_id = Supply.query.filter_by(
            post_id=post.id).first().course_id
        demand_course_id = Demand.query.filter_by(
            post_id=post.id).first().course_id
        supply = dict(
            course_id=supply_course_id,
            course_name=course_api.get_course_by_id(supply_course_id).name)
        demand = dict(
            course_id=demand_course_id,
            course_name=course_api.get_course_by_id(demand_course_id).name)
        p = dict(time=time, supply=supply, demand=demand, message=get_short_message(post.message),
                 id=post.id)
        posts.append(p)
    return render_template('index.html', posts=posts, has_next=has_next,
                           page=page, target_supply=target_supply_text,
                           target_demand=target_demand_text)


@bp.route('/register', methods=['GET', 'POST'])
def register_page(msg=''):
    for m in get_flashed_messages(
            with_categories=False, category_filter=['reg']):
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
    confirm_password = request.values.get('confirmPassword').strip()
    grade = request.values.get('grade').strip()
    email = request.values.get('email').strip()

    if not check_phone(phone):
        return redirect_with_msg(
            '/register', u'你输入的手机号看上去有些奇怪！', category='reg')
    if check_exist(phone):
        return redirect_with_msg(
            '/register', u'此帐号已经被注册了！',
            category='reg')
    if check_email(email) == '':
        return redirect_with_msg(
            '/register', u'你输入的邮箱地址看上去有些奇怪！', category='reg')
    if username == '':
        return redirect_with_msg(
            '/register', u'同学你怎么没有名字啊？！', category='reg')
    min_password_len = 8
    if len(raw_password) < min_password_len:
        return redirect_with_msg(
            '/register', u'密码不能太短喔！', category='reg')
    if raw_password != confirm_password:
        return redirect_with_msg(
            '/register', u'两次密码输入不一致！', category='reg')
    m = hashlib.md5()
    m.update(raw_password.encode('utf-8'))
    password = m.hexdigest()
    user = User(username, phone, email, password, grade)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect('/')


@bp.route('/loginpage', methods=['GET', 'POST'])
def loginpage(msg=''):
    if current_user.is_authenticated:
        return redirect('/')
    for m in get_flashed_messages(
            with_categories=False, category_filter=['login']):
        msg = msg + m
    return render_template('loginpage.html', msg=msg)


@bp.route('/login', methods=['POST'])
def login():
    phone = request.values.get('phone').strip()
    password = request.values.get('password').strip()
    if not check_phone(phone):
        return redirect_with_msg(
            '/loginpage', u'Incorrect format of phone number!',
            category='login')
    if password == '':
        return redirect_with_msg(
            '/loginpage', u'Empty password!', category='login')
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return redirect_with_msg(
            '/loginpage', u'The user does not exist!', category='login')
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    if(m.hexdigest() != user.password):
        return redirect_with_msg(
            '/loginpage', u'Wrong password', category='login')
    login_user(user)
    return redirect('/newpost')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@bp.route('/newpost', methods=['GET', 'POST'])
def newpost_page(msg=''):
    if not current_user.is_authenticated:
        return redirect('/loginpage')
    for m in get_flashed_messages(
            with_categories=False, category_filter=['post']):
        msg = msg + m
    return render_template('newpost.html', msg=msg)


@bp.route('/post', methods=['POST'])
def post():
    user_id = int(current_user.id)
    supply_course_id = int(request.values.get('supplyCourse'))
    demand_course_id = int(request.values.get('demandCourse'))
    if supply_course_id == 31 and demand_course_id == 32:
        return redirect_with_msg(
            '/newpost', u'同学你使用的姿势不正确吼！还要再学习一个！', category='post')
    message = request.values.get('message').strip()
    if not message:
        return redirect_with_msg(
            '/newpost', u'同学你好像什么言都没有留呐！', category='post')
    msg_max_len = 180
    if len(message) > msg_max_len:
        return redirect_with_msg(
            '/newpost', u'同学你留的言太多啦数据库有小情绪了！', category='post')
    created_time = int(time.time())
    p = Post(user_id, created_time, message)
    db.session.add(p)
    db.session.commit()
    d = Demand(int(p.id), demand_course_id)
    s = Supply(int(p.id), supply_course_id)
    db.session.add(d)
    db.session.add(s)
    db.session.commit()
    return redirect('/')


@bp.route('/posts/<int:id>', methods=['GET'])
def posts(id):
    if not current_user.is_authenticated:
        return redirect('/loginpage')
    p = Post.query.get(id)
    u = User.query.get(p.user_id)
    s = Supply.query.filter_by(post_id=id).first()
    d = Demand.query.filter_by(post_id=id).first()
    sc = course_api.get_course_by_id(s.course_id)
    dc = course_api.get_course_by_id(d.course_id)
    scs = CourseSchedule.query.filter_by(course_id=sc.id).all()
    dcs = CourseSchedule.query.filter_by(course_id=dc.id).all()
    supply_schedule = [dict(day=num_to_word(s.day), start=s.start, end=s.end) for s in scs]
    demand_schedule = [dict(day=num_to_word(s.day), start=s.start, end=s.end) for s in dcs]
    user = dict(name=u.name, phone=get_phone_words(u.phone), grade=u.grade)
    supply = dict(name=sc.name, teacher=sc.teacher, credit=sc.credit,
                  schedule=supply_schedule)
    demand = dict(name=dc.name, teacher=dc.teacher, credit=dc.credit,
                  schedule=demand_schedule)
    post = dict(time=timestamp_to_datetime(p.created_time), message=p.message,
                user=user, supply=supply, demand=demand)
    return render_template('post.html', post=post)


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
