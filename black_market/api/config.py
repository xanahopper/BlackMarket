from flask import Blueprint
from black_market.api.utils import normal_jsonify

bp = Blueprint('config', __name__, url_prefix='/config')


@bp.route('', methods=['GET'])
def get_config():
    config = {
        'data_center': False,
    }
    return normal_jsonify(config)
