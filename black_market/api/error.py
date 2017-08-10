from flask import jsonify, Blueprint

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(400)
@bp.app_errorhandler(401)
@bp.app_errorhandler(403)
@bp.app_errorhandler(404)
@bp.app_errorhandler(405)
def handle_4xx_error(error):
    return jsonify(errmsg=error.message), error.http_status_code