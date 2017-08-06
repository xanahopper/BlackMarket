from flask import Blueprint, render_template

from black_market.libs.cache.redis import mc

bp = Blueprint('ssl', __name__)


@bp.route('/.well-known/pki-validation/fileauth.txt', methods=['GET'])
def ssl():
    return '201704061708400y3tan88ebt3rzhgcrzdy2q9o63q3iz95200g9cldqjwpth9iv'
