from flask import Blueprint, render_template, request

from black_market.libs.cache.redis import mc, rd
from black_market.api.utils import normal_jsonify
from black_market.config import RAW_SALT

bp = Blueprint('market', __name__)

index_page_view_count_cache_key = 'black:market:index:view:count'


@bp.route('/', methods=['GET'])
def index():
    rd.incr(index_page_view_count_cache_key)
    page_view = int(rd.get(index_page_view_count_cache_key))
    return render_template('index.html', page_view=page_view)


@bp.route('/clear', methods=['GET'])
def clear():
    data = request.args
    pwd = data.get('pwd')
    if pwd != RAW_SALT:
        return normal_jsonify({'status': 'failed'})
    from manage import init_database
    init_database()
    mc.flushdb()
    return normal_jsonify({'status': 'ok'})


@bp.route('/clear/user/<int:id_>', methods=['GET'])
def clear(id_):
    data = request.args
    pwd = data.get('pwd')
    if pwd != RAW_SALT:
        return normal_jsonify({'status': 'failed'})
    from black_market.model.user.student import Student
    from black_market.model.wechat.session import WechatSession
    student = Student.get(id_)
    name = student.username
    wechat_user = student.wechat_user
    wechat_session = WechatSession.get_by_open_id(wechat_user.open_id)
    student.delete()
    wechat_user.delete()
    wechat_session.delete()
    return normal_jsonify({'status': 'Student %s has been removed.' % name})


@bp.route('/init_post/<int:student_id>', methods=['GET'])
def init_post(student_id):
    import random
    from black_market.model.user.student import Student
    from black_market.model.post.course import CoursePost
    from black_market.model.post.consts import PostMobileSwitch

    student = Student.get(student_id)
    if student:
        supply, demand = random.sample(range(1, 31), 2)
        mobile = student.mobile
        wechat = 'fake_wecaht'
        switch = PostMobileSwitch.on
        message = 'This is the message of student %s!' % student_id
        CoursePost.add(student_id, supply, demand, switch, mobile, wechat, message)
        return normal_jsonify({'status': 'ok'})
    return normal_jsonify({}, 'No student %s! Please create student before init post' % student_id)
