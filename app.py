from black_market.app import create_app
from black_market.config import HTTP_PORT
from werkzeug.contrib.fixers import ProxyFix


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=HTTP_PORT)
