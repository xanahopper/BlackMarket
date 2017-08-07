from flask import request, abort, jsonify

from black_market.api._bp import create_blueprint
from black_market.api.schema import student as student_schema
from black_market.config import DEBUG
from black_market.libs.sms.sms import SMS
from black_market.libs.sms.templates import VERIFY_CODE_TEMPLATE
from black_market.model.code.consts import SMSVerifyType
from black_market.model.code.verify import SMSVerify
from black_market.model.exceptions import InvalidSMSVerifyCodeError, RequestFailedError
from black_market.model.user.consts import AccountStatus, StudentType
from black_market.model.user.student import Student
from black_market.model.wechat.session import WechatSession
from black_market.model.wechat.user import WechatUser
from black_market.model.utils import validator

bp = create_blueprint('student', 'v1', __name__, url_prefix='/student')


@bp.route('/<int:id_>', methods=['GET'])
def get_student(id_):
    student = Student.get(id_)
    if not student:
        abort(404)
    return jsonify(student.dump())


@bp.route('/register', methods=['POST'])
def send_register_code():
    data = student_schema.RegisterStudentSchema().fill()
    mobile = data.get('mobile')
    validator.validate_phone(mobile)
    code = SMSVerify.add(mobile, SMSVerifyType.register)
    msg = VERIFY_CODE_TEMPLATE.format(code=code)
    SMS.send(mobile, msg, tag='register')
    if DEBUG:
        return jsonify(code=code, msg=msg)
    return jsonify({})


@bp.route('/', methods=['POST'])
def create_user():
    data = student_schema.CreateStudentSchema().fill()

    wechat_session = WechatSession.get_by_third_session_key(data['session_key'])
    if not wechat_session:
        abort(404)
    open_id = wechat_session.open_id

    mobile = data['mobile']
    validator.validate_phone(mobile)

    verify_code = data['verify_code']
    r = SMSVerify.verify(mobile, verify_code, SMSVerifyType.register)
    if not r:
        raise InvalidSMSVerifyCodeError

    type_ = StudentType(data['type'])
    grade = data['grade']
    wechat_user = WechatUser.get_by_open_id(open_id)
    id_ = wechat_user.id
    id_ = Student.add(id_, mobile, open_id, type_, grade, AccountStatus.need_verify)

    if not id_:
        raise RequestFailedError

    return jsonify({})


@bp.route('/', methods=['PUT'])
def edit_user():
    # TODO
    return jsonify({})
