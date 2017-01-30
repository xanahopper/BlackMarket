import logging
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from black_market.config import SENTRY_DSN

sentry = Sentry(logging=True, level=logging.ERROR, dsn=SENTRY_DSN)
db = SQLAlchemy()
login_manager = LoginManager()
