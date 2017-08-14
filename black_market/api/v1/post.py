from flask import g

from .._bp import create_blueprint
from black_market.model.user.student import Student
from black_market.model.post.course import CoursePost
from black_market.model.post.consts import PostMobileSwitch
from black_market.model.post.consts import OrderType

from black_market.api.utils import normal_jsonify
from black_market.api.decorator import require_session_key
from black_market.api.schema.post import (
    CreateCoursePostSchema, UpdateCoursePostSchema, GetCoursePostSchema)

bp = create_blueprint('course.post', 'v1', __name__, url_prefix='/course/post')


@bp.route('/', methods=['GET'])
@require_session_key()
def get_posts():
    data = GetCoursePostSchema().fill()
    start = data.get('start', 0)
    limit = data.get('limit', 10)
    order = OrderType(data.get('order', 0))
    supply = data.get('supply', None)
    demand = data.get('demand', None)
    posts = CoursePost.gets(
        limit=limit, offset=start, order=order, supply=supply, demand=demand)
    if posts:
        return normal_jsonify([post.dump() for post in posts])
    return normal_jsonify([])


@bp.route('/', methods=['POST'])
@require_session_key()
def create_post():
    data = CreateCoursePostSchema().fill()
    student_id = data['student_id']
    supply = data['supply']
    demand = data['demand']
    switch = PostMobileSwitch(data['switch'])
    mobile = data['mobile']
    wechat = data['wechat']
    message = data['message']
    post = CoursePost.add(student_id, supply, demand, switch, mobile, wechat, message)
    return normal_jsonify(post.dump())


@bp.route('/<int:post_id>', methods=['GET'])
@require_session_key()
def get_post(post_id):
    post = CoursePost.get(post_id)
    student = Student.get(g.wechat_user.id)
    if student.id != post.student_id:
        post.pv += 1
    return normal_jsonify(post.dump())


@bp.route('/<int:post_id>', methods=['PUT'])
@require_session_key()
def edit_post(post_id):
    data = UpdateCoursePostSchema().fill()
    post = CoursePost.get(post_id)
    post.update_self(data)
    return normal_jsonify({'status': 'ok'})
