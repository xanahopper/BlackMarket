from flask import Blueprint

from black_market.model.exceptions import BlackMarketError

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(400)
@bp.app_errorhandler(401)
@bp.app_errorhandler(403)
@bp.app_errorhandler(404)
@bp.app_errorhandler(405)
def handle_4xx_error(error):
    # return jsonify(errmsg=error.description, code=0), error.code
    raise error


@bp.app_errorhandler(BlackMarketError)
def handle_biz_error(error):
    raise error
    # return jsonify(errmsg=error.message, code=error.code), error.http_status_code
