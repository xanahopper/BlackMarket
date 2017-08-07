# from flask import jsonify
from .._bp import create_blueprint


bp = create_blueprint('course', 'v1', __name__, url_prefix='/course')


# @bp.route('/course/<int:limit>/<int:offset>', methods=['GET'])
# def get_courses(limit, offset):
#     # courses = Course.gets(limit=limit, offset=offset)
#     # return normal_jsonify([course.dict_ for course in courses])
#     return
#
#
# @bp.route('/course/<int:course_id>', methods=['GET'])
# def get_course(course_id):
#     # return normal_jsonify(Course.get(course_id).dict_)
#     return
#
#
# @bp.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     # return normal_jsonify(User.get(user_id).dict_)
#     return


# @bp.route('/', methods=['GET'])
# def get():
#     return jsonify(openid='1111', session_key='2222', unionid='3333')
