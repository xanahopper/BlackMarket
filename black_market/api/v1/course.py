from flask import abort

from .._bp import create_blueprint
from black_market.api.utils import normal_jsonify
from black_market.api.decorator import require_session_key
from black_market.model.course import Course

bp = create_blueprint('course', 'v1', __name__, url_prefix='/course')


@bp.route('/<int:course_id>', methods=['GET'])
@require_session_key()
def get_course(course_id):
    course = Course.get(course_id)
    if course:
        return normal_jsonify(course.dump())
    abort(404)


@bp.route('/', methods=['GET'])
@require_session_key()
def get_courses():
    courses = Course.get_all()
    return normal_jsonify([course.dump() for course in courses])
