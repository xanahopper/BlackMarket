from datetime import datetime, timedelta
from werkzeug.utils import cached_property
from black_market.ext import db
from .client import OAuthClient


class OAuthGrant(db.Model):
    __tablename__ = 'oauth_grant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer)
    code = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    scopes = db.Column(db.String(80))
    redirect_uri = db.Column(db.String(80))
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, client_id, code, user_id, scopes, redirect_uri):
        self.client_id = client_id
        self.code = code
        self.user_id = user_id
        self.scopes = scopes
        self.redirect_uri = redirect_uri

    @cached_property
    def expires(self):
        return self.create_time + timedelta(seconds=120)

    @cached_property
    def user(self):
        return self.user_class.get(self.user_id)

    @cached_property
    def user_class(self):
        from black_market.model.user.consts import AccountType
        from black_market.model.user.student import Student
        if not self.client:
            raise ValueError
        if self.client.account_type is AccountType.student:
            return Student
        raise ValueError

    @cached_property
    def client(self):
        return OAuthClient.get(self.client_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def add(cls, client_id, code, redirect_uri, scopes, user_id):
        scopes = ','.join(scope.strip() for scope in scopes)
        oauth_grant = OAuthGrant(client_id, code, user_id, scopes, redirect_uri)
        db.session.add(oauth_grant)
        db.session.commit()
        return oauth_grant.id

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_code(cls, client_id, code):
        return cls.query.filter_by(client_id=client_id, code=code).first()
