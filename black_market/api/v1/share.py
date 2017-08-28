from flask import send_file

from black_market.api.schema.share import SharePostSchema, ShareMeSchema
from black_market.api.utils import normal_jsonify
from black_market.model.post.consts import PostType
from black_market.model.user.student import Student
from black_market.model.user.behavior import UserBehavior
from black_market.model.user.consts import UserBehaviorType
from black_market.service.image.share_me import create_share_me_image
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


@bp.route('/me/image', methods=['POST'])
def share_me_image():
    data = ShareMeSchema().fill()
    student_id = data.get('student_id')
    student = Student.get(student_id)

    img_io = create_share_me_image(student)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')
