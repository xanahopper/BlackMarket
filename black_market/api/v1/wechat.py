import requests
from flask import request, jsonify, abort

from black_market.api._bp import create_blueprint
from black_market.intergration.wechat import wechat
from black_market.model.wechat.session import WechatSession

bp = create_blueprint('wechat', 'v1', __name__, url_prefix='/wechat')


@bp.route('/jscode2session', methods=['GET'])
def jscode2session():
    """Exchange Jscode for Session"""

    data = request.args.to_dict()
    code = data.get('code')

    r = wechat.jscode2session(js_code=code)
    res = r.json()
    if r.status_code == requests.codes.ok:
        open_id = res['openid']
        session_key = res['session_key']
        third_session_key = WechatSession.add(open_id, session_key)
        return jsonify(session_key=third_session_key)
    errcode = res.get('errcode') or ''
    errmsg = res.get('errmsg') or ''
    return jsonify(errcode=errcode, errmsg=errmsg), 401


@bp.route('/check_session', methods=['GET'])
def check_session():
    """Check Session"""
    data = request.args.to_dict()
    third_session_key = data.get('session_key')
    wechat_session = WechatSession.get_by_third_session_key(third_session_key)
    if wechat_session:
        return jsonify({})
    abort(404)
