from flask import g

from .._bp import create_blueprint
from black_market.model.user.student import Student
from black_market.model.user.view_record import ViewRecord
from black_market.model.user.behavior import UserBehavior
from black_market.model.user.consts import UserBehaviorType
from black_market.model.post.goods import GoodsPost
from black_market.model.post.consts import PostMobileSwitch
from black_market.model.post.consts import OrderType, PostStatus, PostType

from black_market.api.utils import normal_jsonify
from black_market.api.decorator import require_session_key
from black_market.api.schema.post import (
    CreateGoodsPostSchema, UpdateGoodsPostSchema,
    UpdateGoodsPostStatusSchema, GetGoodsPostSchema,
    DecrRemainingViewCountSchema)

bp = create_blueprint('goods.post', 'v1', __name__, url_prefix='/goods/post')


@bp.route('/', methods=['GET'])
@require_session_key()
def get_posts():
    data = GetGoodsPostSchema().fill()
    start = data.get('start', 0)
    limit = data.get('limit', 10)
    order = OrderType(data.get('order', 0))
    posts = GoodsPost.gets(limit=limit, offset=start, order=order)
    if posts:
        return normal_jsonify([post.dump() for post in posts])
    return normal_jsonify([])


@bp.route('/', methods=['POST'])
@require_session_key()
def create_post():
    data = CreateGoodsPostSchema().fill()
    student_id = data['student_id']
    switch = PostMobileSwitch(data['switch'])
    mobile = data['mobile']
    wechat = data['wechat']
    message = data['message']
    imgs = data['imgs']
    post = GoodsPost.add(student_id, switch, mobile, wechat, imgs, message)
    UserBehavior.add(g.wechat_user.id, UserBehaviorType.create_goods_post, dict(post_id=post.id))
    return normal_jsonify(post.dump())


@bp.route('/<int:post_id>', methods=['GET'])
@require_session_key()
def get_post(post_id):
    post = GoodsPost.get(post_id)
    student = Student.get(g.wechat_user.id)
    if student.id != post.student_id:
        post.pv += 1
    has_viewed_contact = True if ViewRecord.gets(
        student.id, post_id, PostType.goods_post) else False
    UserBehavior.add(g.wechat_user.id, UserBehaviorType.view_goods_post, dict(post_id=post_id))
    return normal_jsonify(dict(post=post.dump(), has_viewed_contact=has_viewed_contact))


@bp.route('/<string:fuzzy_post_id>', methods=['GET'])
def get_post_from_fuzzy(fuzzy_post_id):
    post_id = GoodsPost.defuzzy(fuzzy_post_id)
    post = GoodsPost.get(post_id)
    post.pv += 1
    return normal_jsonify(dict(post=post.share_dump()))


@bp.route('/<int:post_id>', methods=['PUT'])
@require_session_key()
def edit_post(post_id):
    data = UpdateGoodsPostSchema().fill()
    post = GoodsPost.get(post_id)
    post.update_self(data)
    UserBehavior.add(g.wechat_user.id, UserBehaviorType.edit_goods_post, dict(post_id=post_id))
    return normal_jsonify({'status': 'ok'})


@bp.route('/<int:post_id>/status', methods=['PUT'])
@require_session_key()
def edit_post_status(post_id):
    data = UpdateGoodsPostStatusSchema().fill()
    status = PostStatus(data['status'])
    post = GoodsPost.get(post_id)
    post.update_status(status)
    UserBehavior.add(g.wechat_user.id, UserBehaviorType.markdone_goods_post,
                     dict(post_id=post_id, status=status.value))
    return normal_jsonify({'status': 'ok'})


@bp.route('/viewcount', methods=['GET'])
@require_session_key()
def get_remaining_viewcount():
    student = Student.get(g.wechat_user.id)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    viewcount = student.remaining_viewcount
    return normal_jsonify(dict(viewcount=viewcount))


@bp.route('/viewcount', methods=['PUT'])
@require_session_key()
def decr_remaining_viewcount():
    student = Student.get(g.wechat_user.id)
    if not student:
        return normal_jsonify({}, 'Student Not Found', 404)
    data = DecrRemainingViewCountSchema().fill()
    post_id = data['post_id']
    student.decr_viewcount()
    ViewRecord.add(student.id, post_id, PostType.goods_post)
    UserBehavior.add(
        g.wechat_user.id, UserBehaviorType.view_goods_post_contact, dict(post_id=post_id))
    return normal_jsonify({})
