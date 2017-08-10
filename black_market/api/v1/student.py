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
    InvalidSMSVerifyCodeError, SendSMSTooManyTimesError, AtemptTooManyTimesError)
from black_market.model.user.consts import AccountStatus, StudentType
from black_market.model.user.student import Student
from black_market.model.utils import validator

bp = create_blueprint('student', 'v1', __name__, url_prefix='/student')


@bp.route('/', methods=['GET'])
@require_session_key()
def get_student():
    wechat_user = g.wechat_user
    id_ = wechat_user.id
    student = Student.get(id_)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
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
    return normal_jsonify(student.dump())


@bp.route('/register', methods=['POST'])
@require_session_key(require_wechat_user=False)
def send_register_code():
    data = student_schema.RegisterStudentSchema().fill()
    mobile = data.get('mobile')
    validator.validate_phone(mobile)

    try:
        code = SMSVerify.add(mobile, SMSVerifyType.register)
    except SendSMSTooManyTimesError as e:
        return normal_jsonify({}, e.message, e.http_status_code)

    msg = VERIFY_CODE_TEMPLATE.format(code=code)
    SMS.send(mobile, msg, tag='register')
    if DEBUG:
        return normal_jsonify(dict(code=code, msg=msg))
    return normal_jsonify({})
