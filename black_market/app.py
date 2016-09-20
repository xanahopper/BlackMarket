from flask import Flask
from werkzeug.utils import import_string
from black_market.config import SECRET_KEY

extensions = [
    'black_market.ext:sentry'
]

blueprints = [
    'black_market.views.market.market:bp'
]


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('envcfg.json.black_market')
    app.config.from_object(config)
    app.secret_key = SECRET_KEY
    for ext_name in extensions:
        extension = import_string(ext_name)
        extension.init_app(app)

    for blueprint_name in blueprints:
        blueprint = import_string(blueprint_name)
        app.register_blueprint(blueprint)

    return app
