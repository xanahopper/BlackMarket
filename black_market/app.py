from flask import Flask
from werkzeug.utils import import_string
from black_market.config import SECRET_KEY, MYSQL_DSN

extensions = [
    'black_market.ext:db',
    'black_market.ext:login_manager'
]

blueprints = [
    'black_market.views.market.market:bp'
]


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('envcfg.json.black_market')
    app.config.from_object(config)
    app.secret_key = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_DSN
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
    for ext_name in extensions:
        extension = import_string(ext_name)
        extension.init_app(app)

    for blueprint_name in blueprints:
        blueprint = import_string(blueprint_name)
        app.register_blueprint(blueprint)

    return app
