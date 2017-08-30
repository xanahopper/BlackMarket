from flask import send_file

from black_market.api.schema.share import (
    SharePostSchema, ShareStudentSchema, GetShareStudentImageSchema,
    GetSharePostImageSchema)
from black_market.api.utils import normal_jsonify
from black_market.model.post.consts import PostType
from black_market.model.post.course import CoursePost
from black_market.model.course import Course
from black_market.model.user.student import Student
from black_market.model.user.behavior import UserBehavior
from black_market.model.user.consts import UserBehaviorType
from black_market.model.exceptions import UserNotFoundError, PostNotFoundError
from black_market.service.image.share_me import create_share_me_image
from black_market.service.image.share_post import create_share_post_image
from .._bp import create_blueprint

bp = create_blueprint('share', 'v1', __name__, url_prefix='/share')


@bp.route('/post', methods=['POST'])
def share_post():
    data = SharePostSchema().fill()

    post_id = data.get('post_id')
    post_type = PostType(data.get('post_type'))
    student_id = data.get('student_id', 0)
    detail = dict(post_id=post_id, student_id=student_id)
    if post_type is PostType.course_post:
        UserBehavior.add(student_id, UserBehaviorType.share_course_post, detail)
    elif post_type is PostType.goods_post:
        UserBehavior.add(student_id, UserBehaviorType.share_goods_post, detail)
    return normal_jsonify()


@bp.route('/student', methods=['POST'])
def share_student():
    data = ShareStudentSchema().fill()
    student_id = data.get('student_id')
    UserBehavior.add(student_id, UserBehaviorType.share_me_to_friend)
    return normal_jsonify()


@bp.route('/student/<int:student_id>/image', methods=['GET'])
def get_share_student_image(student_id):
    data = GetShareStudentImageSchema().fill()
    path = data.get('path') or 'pages/index?query=1'
    student = Student.get(student_id)
    if not student:
        raise UserNotFoundError()

    img_io = create_share_me_image(student, path)
    img_io.seek(0)

    UserBehavior.add(student_id, UserBehaviorType.get_share_me_image)
    return send_file(img_io, mimetype='image/jpeg')


@bp.route('/post/<int:post_id>/image', methods=['GET'])
def get_share_post_image(post_id):
    data = GetSharePostImageSchema().fill()

    path = data.get('path', 'pages/splash/splash')
    supply = data.get('supply', None)
    demand = data.get('demand', None)
    student_id = data.get('student_id', None)

    post = CoursePost.get(post_id)
    if not post:
        raise PostNotFoundError()
    student = Student.get(post.student_id)
    if not student:
        raise UserNotFoundError()

    supply_course_name = None
    demand_course_name = None
    supply_course = Course.get(supply) if supply else None
    demand_course = Course.get(demand) if demand else None
    if supply_course:
        supply_course_name = supply_course.name
    if demand_course:
        demand_course_name = demand_course.name

    img_io = create_share_post_image(student, path, supply_course_name, demand_course_name)
    img_io.seek(0)

    UserBehavior.add(student_id or student.id, UserBehaviorType.get_share_course_post_image)
    return send_file(img_io, mimetype='image/jpeg')
