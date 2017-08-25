from .._bp import create_blueprint
from black_market.api.utils import normal_jsonify
from black_market.api.schema.share import SharePostSchema
from black_market.model.post.consts import PostType
from black_market.model.user.behavior import UserBehavior
from black_market.model.user.consts import UserBehaviorType


bp = create_blueprint('share', 'v1', __name__, url_prefix='/post/share')


@bp.route('', methods=['POST'])
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
