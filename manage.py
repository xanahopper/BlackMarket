from flask_script import Manager

from black_market.app import create_app
from black_market.ext import db

app = create_app()
manager = Manager(app)


@manager.command
def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    manager.run()
