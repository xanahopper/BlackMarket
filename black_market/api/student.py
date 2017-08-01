from flask import request, abort, jsonify
from oauthlib.common import generate_token

from black_market.api.decorator import require_oauth, require_credentials
from black_market.model.user.student import Student
from black_market.model.user.consts import AccountStatus, StudentType, Gender
from black_market.model.oauth.scopes import OAuthScope
from black_market.model.oauth.token import OAuthToken
from black_market.model.exceptions import (
    InvalidValueError, InvalidSMSVerifyCodeError, RequestFailedError)
from black_market.model.utils import validator

from black_market.api.schema import student as student_schema
from ._bp import create_blueprint


bp = create_blueprint('student', __name__, url_prefix='/student')


@bp.route('/<int:id_>', methods=['GET'])
@require_oauth(scopes=[OAuthScope.student])
def get_student(id_):
    student = Student.get(id_)
    if not student:
        abort(404)
    return jsonify(student.dump())

#
# @bp.route('/@<string:username>', methods=['GET'])
# def get_user_by_username(username):
#     return 'Student %s' % username


@bp.route('/', methods=['POST'])
@require_credentials(scopes=[OAuthScope.student])
def create_user():
    client = request.oauth_client
    data = student_schema.CreateStudentSchema().fill()
    mobile = data['mobile']
    raw_password = data['raw_password']
    password_repeat = data['password_repeat']

    validator.validate_phone(mobile)

    if raw_password != password_repeat:
        raise InvalidValueError

    validator.validate_password(raw_password)

    # TODO
    verify_code = data.get('verify_code')

    # r = SMSVerify.verify(mobile, verify_code, SMSVerifyType.register)
    # if not r:
    #     raise InvalidSMSVerifyCodeError

    name = data['name']
    gender = Gender(data['gender'])
    type_ = StudentType(data['type'])
    grade = data['grade']
    id_ = Student.add(name, gender, grade, type_, raw_password, mobile, AccountStatus.need_verify)

    if not id_:
        raise RequestFailedError

    student = Student.get(id_)

    access_token = generate_token()
    refresh_token = generate_token()

    allowed_scopes = [OAuthScope.student]
    scopes = [scope.name for scope in allowed_scopes]

    id_ = OAuthToken.add(client.id, id_, scopes, access_token, refresh_token)
    token = OAuthToken.get(id_)
    return jsonify(student=student.dump(), token=token.dump())

# @bp.route('/', methods=['PUT'])
# def edit_user(message=''):
#     # form_data = request.form
#     # user_id = current_user.id
#     # try:
#     #     pass
#     # except UserException as e:
#     #     message = e.message
#     # return normal_jsonify(data='', message=message)
#     return
