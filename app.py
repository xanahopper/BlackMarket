from werkzeug.contrib.fixers import ProxyFix

from black_market.app import create_app
from black_market.config import DEBUG, HTTP_HOST, HTTP_PORT

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host=HTTP_HOST, port=HTTP_PORT)
