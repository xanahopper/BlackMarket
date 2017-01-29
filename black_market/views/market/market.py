from flask import Blueprint, request, render_template, redirect

from black_market.libs.api import course as course_api

from black_market.models.models import Post, Supply, Demand

bp = Blueprint('market', __name__)


def timestamp_to_datetime(timestamp):
    return timestamp


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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
