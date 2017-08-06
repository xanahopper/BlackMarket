from flask import request, abort, jsonify
from urllib.parse import urlparse, unquote_plus

from black_market.api._bp import create_blueprint
from black_market.intergration.wechat import wechat

bp = create_blueprint('wechat', __name__, url_prefix='/wechat')


@bp.route('/jsconfig', methods=['GET'])
def get_jsapi_config():
    """获取服务号JSAPI的配置参数"""

    data = request.args.to_dict()
    url = data.get('url')
    parsed = urlparse(unquote_plus(url))
    if not parsed.hostname:
        abort(403)

    config = wechat.get_jsapi_config(url=parsed.geturl())
    return jsonify(config)
