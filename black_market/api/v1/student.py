# from flask import request, abort, jsonify
# from oauthlib.common import generate_token
#
# from black_market.api._bp import create_blueprint
# from black_market.api.schema import student as student_schema
# from black_market.config import DEBUG
# from black_market.libs.sms.sms import SMS
# from black_market.libs.sms.templates import VERIFY_CODE_TEMPLATE
# from black_market.model.code.consts import SMSVerifyType
# from black_market.model.code.verify import SMSVerify
# from black_market.model.exceptions import (
#     InvalidValueError, InvalidSMSVerifyCodeError, RequestFailedError)
# from black_market.model.user.consts import AccountStatus, StudentType, Gender
# from black_market.model.user.student import Student
# from black_market.model.utils import validator
#
# bp = create_blueprint('student', 'v1', __name__, url_prefix='/student')
#
#
# @bp.route('/<int:id_>', methods=['GET'])
# def get_student(id_):
#     student = Student.get(id_)
#     if not student:
#         abort(404)
#     return jsonify(student.dump())
#
#
# @bp.route('/', methods=['POST'])
# def create_user():
#     client = request.oauth_client
#     data = student_schema.CreateStudentSchema().fill()
#     mobile = data['mobile']
#     raw_password = data['raw_password']
#     password_repeat = data['password_repeat']
#
#     validator.validate_phone(mobile)
#
#     if raw_password != password_repeat:
#         raise InvalidValueError
#
#     validator.validate_password(raw_password)
#
#     # TODO
#     verify_code = data.get('verify_code')
#
#     r = SMSVerify.verify(mobile, verify_code, SMSVerifyType.register)
#     if not r:
#         raise InvalidSMSVerifyCodeError
#
#     name = data['name']
#     gender = Gender(data['gender'])
#     type_ = StudentType(data['type'])
#     grade = data['grade']
#     id_ = Student.add(name, gender, grade, type_, raw_password, mobile, AccountStatus.need_verify)
#
#     if not id_:
#         raise RequestFailedError
#
#     student = Student.get(id_)
#
#     access_token = generate_token()
#     refresh_token = generate_token()
#
#     allowed_scopes = [OAuthScope.student]
#     scopes = [scope.name for scope in allowed_scopes]
#
#     id_ = OAuthToken.add(client.id, id_, scopes, access_token, refresh_token)
#     token = OAuthToken.get(id_)
#     return jsonify(student=student.dump(), token=token.dump())
#
#
# @bp.route('/register', methods=['POST'])
# def send_register_code():
#     body = request.get_json()
#     mobile = body.get('mobile')
#     validator.validate_phone(mobile)
#     code = SMSVerify.add(mobile, SMSVerifyType.register)
#     msg = VERIFY_CODE_TEMPLATE.format(code=code)
#     SMS.send(mobile, msg, tag='register')
#     if DEBUG:
#         return jsonify(code=code)
#     return jsonify({'mobile': mobile})
#
#
# # @bp.route('/', methods=['PUT'])
# # def edit_user(message=''):
# #     # form_data = request.form
# #     # user_id = current_user.id
# #     # try:
# #     #     pass
# #     # except UserException as e:
# #     #     message = e.message
# #     # return normal_jsonify(data='', message=message)
# #     return
