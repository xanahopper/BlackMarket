import logging

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from raven.contrib.flask import Sentry

from black_market.config import SENTRY_DSN


sentry = Sentry(logging=True, level=logging.ERROR, dsn=SENTRY_DSN)
db = SQLAlchemy()
ma = Marshmallow()
