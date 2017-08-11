from flask import Blueprint, render_template

from black_market.libs.cache.redis import mc, rd
from black_market.api.utils import normal_jsonify

bp = Blueprint('market', __name__)

index_page_view_count_cache_key = 'black:market:index:view:count'


@bp.route('/', methods=['GET'])
def index():
    rd.incr(index_page_view_count_cache_key)
    page_view = int(rd.get(index_page_view_count_cache_key))
    return render_template('index.html', page_view=page_view)


@bp.route('/clear', methods=['GET'])
def clear():
    from manage import init_database
    init_database()
    mc.flushdb()
    return normal_jsonify({'status': 'ok'})


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
