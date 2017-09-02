from flask import jsonify, g

from black_market.api._bp import create_blueprint
from black_market.api.decorator import require_session_key
from black_market.api.utils import normal_jsonify
from black_market.api.schema import student as student_schema
from black_market.config import DEBUG
from black_market.libs.sms.sms import SMS
from black_market.libs.sms.templates import VERIFY_CODE_TEMPLATE
from black_market.model.code.consts import SMSVerifyType
from black_market.model.code.verify import SMSVerify
from black_market.model.exceptions import (
    InvalidSMSVerifyCodeError, AtemptTooManyTimesError, MobileAlreadyExistedError)
from black_market.model.user.consts import AccountStatus, StudentType, UserBehaviorType
from black_market.model.user.student import Student
from black_market.model.user.behavior import UserBehavior
from black_market.model.post.course import CoursePost
from black_market.model.post.consts import OrderType
from black_market.model.utils import validator

bp = create_blueprint('student', 'v1', __name__, url_prefix='/student')


@bp.route('/', methods=['GET'])
@require_session_key()
def get_current_student():
    wechat_user = g.wechat_user
    id_ = wechat_user.id
    student = Student.get(id_)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    return jsonify(student.dump())


@bp.route('/post', methods=['GET'])
@require_session_key()
def get_my_post():
    student = Student.get(g.wechat_user.id)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    data = student_schema.GetMyCoursePostSchema().fill()
    start = data.get('start', 0)
    limit = data.get('limit', 10)
    order = OrderType(data.get('order', 0))
    posts = CoursePost.gets_by_student(
        student.id, limit=limit, offset=start, order=order)
    return jsonify([post.dump() for post in posts])


@bp.route('/<int:student_id>/post', methods=['GET'])
@require_session_key()
def get_posts_by_student(student_id):
    student = Student.get(student_id)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    data = student_schema.GetMyCoursePostSchema().fill()
    start = data.get('start', 0)
    limit = data.get('limit', 10)
    order = OrderType(data.get('order', 0))
    posts = CoursePost.gets_by_student(
        student.id, limit=limit, offset=start, order=order)
    UserBehavior.add(
        g.wechat_user.id, UserBehaviorType.view_other_posts, dict(student_id=student_id))
    return jsonify([post.dump() for post in posts])


@bp.route('/share/profile/<int:student_id>', methods=['GET'])
def get_student_share_profile(student_id):
    student = Student.get(student_id)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    return jsonify(student.share_dump())


@bp.route('/<int:student_id>', methods=['GET'])
@require_session_key()
def get_student(student_id):
    student = Student.get(student_id)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    UserBehavior.add(
        g.wechat_user.id, UserBehaviorType.view_other_profile, dict(student_id=student_id))
    return jsonify(student.dump())


@bp.route('/', methods=['POST'])
@require_session_key()
def create_user():
    wechat_user = g.wechat_user
    open_id = wechat_user.open_id

    data = student_schema.CreateStudentSchema().fill()
    mobile = data['mobile']
    validator.validate_phone(mobile)

    verify_code = data['verify_code']

    try:
        r = SMSVerify.verify(mobile, verify_code, SMSVerifyType.register)
    except AtemptTooManyTimesError as e:
        return normal_jsonify({}, e.message, e.http_status_code)

    if not r:
        raise InvalidSMSVerifyCodeError()

    type_ = StudentType(data['type'])
    grade = data['grade']
    id_ = Student.add(wechat_user.id, mobile, open_id, type_, grade, AccountStatus.need_verify)
    student = Student.get(id_)
    SMS.reg_complete.delay(mobile=mobile)
    Student.cache_avatar.delay(student.id, student.avatar_url)
    return normal_jsonify(student.dump())


@bp.route('/', methods=['PUT'])
@require_session_key()
def update_user():
    data = student_schema.UpdateStudentSchema().fill()
    type_ = StudentType(data['type'])
    grade = data['grade']
    wechat_user = g.wechat_user
    id_ = wechat_user.id
    student = Student.get(id_)
    student = student.update(type_, grade)
    UserBehavior.add(
        g.wechat_user.id, UserBehaviorType.edit_profile, dict(type_=type_.value, grade=grade))
    return normal_jsonify(student.dump())


@bp.route('/register', methods=['POST'])
@require_session_key(require_wechat_user=False)
def send_register_code():
    data = student_schema.RegisterStudentSchema().fill()
    mobile = data.get('mobile')
    validator.validate_phone(mobile)
    if Student.existed(mobile):
        raise MobileAlreadyExistedError()
    code = SMSVerify.add(mobile, SMSVerifyType.register)
    msg = VERIFY_CODE_TEMPLATE.format(code=code)
    SMS.send(mobile, msg, tag='register')
    if DEBUG:
        print(msg)
        return normal_jsonify(dict(code=code, msg=msg))
    return normal_jsonify({})
