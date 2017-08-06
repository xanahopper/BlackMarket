from flask import Blueprint

from black_market.config import SSL_FILEAUTH_TEXT


bp = Blueprint('ssl', __name__)


@bp.route('/.well-known/pki-validation/fileauth.txt', methods=['GET'])
def ssl():
    return SSL_FILEAUTH_TEXT
