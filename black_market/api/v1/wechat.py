from flask import request, jsonify, g

from black_market.api._bp import create_blueprint
from black_market.api.utils import normal_jsonify
from black_market.api.decorator import require_session_key
from black_market.intergration.wechat import wechat
from black_market.model.wechat.session import WechatSession
from black_market.model.wechat.user import WechatUser

bp = create_blueprint('wechat', 'v1', __name__, url_prefix='/wechat')


@bp.route('/jscode2session', methods=['GET'])
def jscode2session():
    """Exchange Jscode for Session"""

    data = request.args.to_dict()
    code = data.get('code')

    r = wechat.jscode2session(code)
    res = r.json()
    if res.get('openid') and res.get('session_key'):
        open_id = res.get('openid')
        session_key = res.get('session_key')
        third_session_key = WechatSession.add(open_id, session_key)
        return jsonify(session_key=third_session_key)
    errcode = res.get('errcode') or ''
    errmsg = res.get('errmsg') or ''
    return jsonify(errcode=errcode, errmsg=errmsg), 401


@bp.route('/check_session', methods=['GET'])
@require_session_key(require_wechat_user=False)
def check_session():
    """Check Session"""
    return normal_jsonify({})


@bp.route('/user', methods=['POST', 'PUT'])
@require_session_key(require_wechat_user=False)
def update_wechat_user():
    wechat_session = g.wechat_session
    open_id = wechat_session.open_id
    data = request.get_json()
    user_info = data['userInfo']
    nickname = user_info.get('nickName')
    gender = user_info.get('gender')
    language = user_info.get('language')
    city = user_info.get('city')
    province = user_info.get('province')
    country = user_info.get('country')
    avatar_url = user_info.get('avatarUrl')

    WechatUser.add(open_id, nickname, avatar_url, city,
                   country, gender, language, province)
    return normal_jsonify({})
