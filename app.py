import logging
from time import strftime
from logging.handlers import RotatingFileHandler

from flask import request
from flask_login import current_user
from werkzeug.contrib.fixers import ProxyFix

from black_market.app import create_app
from black_market.config import HTTP_PORT


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s %s %s', timestamp, current_user.id,
                 request.remote_addr, request.method, request.scheme,
                 request.full_path, response.status)
    return response


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)

    app.debug = True
    app.run(host='0.0.0.0', port=HTTP_PORT)
