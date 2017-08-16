from flask import Blueprint
from black_market.api.utils import normal_jsonify

bp = Blueprint('health', __name__, url_prefix='/health')


@bp.route('', methods=['GET'])
def health():
    return normal_jsonify({'status': 'ok'})
