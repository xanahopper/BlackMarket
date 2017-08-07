from flask import Flask
from werkzeug.utils import import_string

extensions = [
    'black_market.ext:db',
    'black_market.ext:ma',
    'black_market.ext:oauth_server',
]

blueprints = [
    'black_market.views.market:bp',
    'black_market.api.ssl:bp',
    'black_market.api.v1.oauth:bp',
    'black_market.api.v1.student:bp',
    'black_market.api.v1.course:bp',
]


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('envcfg.json.black_market')
    app.config.from_object(config)
    for ext_name in extensions:
        extension = import_string(ext_name)
        extension.init_app(app)

    for blueprint_name in blueprints:
        blueprint = import_string(blueprint_name)
        app.register_blueprint(blueprint)

    return app
