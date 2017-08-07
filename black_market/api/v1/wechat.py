from flask import request, jsonify

from black_market.api._bp import create_blueprint
from black_market.intergration.wechat import wechat

bp = create_blueprint('wechat', 'v1', __name__, url_prefix='/wechat')


@bp.route('/jscode2session', methods=['GET'])
def jscode2session():
    """获取服务号JSAPI的配置参数"""

    data = request.args.to_dict()
    code = data.get('code')

    r = wechat.jscode2session(js_code=code)
    res = r.json()
    return jsonify(res)
    # open_id = res['openid']
    # session_key = res['session_key']
    # unionid = res['unionid']
