from oauthlib.common import generate_token
from werkzeug.utils import cached_property

from black_market.ext import db
from black_market.model.user.consts import AccountType
from .consts import ClientStatus
from .scopes import OAuthScope


class OAuthClient(db.Model):
    __tablename__ = 'oauth_client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    status_ = db.Column(db.SmallInteger)
    client_id = db.Column(db.String(80))
    client_secret = db.Column(db.String(80))
    account_type_ = db.Column(db.SmallInteger)
    allowed_scopes_ = db.Column(db.String(80))
    redirect_uri = db.Column(db.String(80))

    def __init__(self, name, status, client_id, client_secret,
                 account_type, allowed_scopes, redirect_uri):
        self.name = name
        self.status_ = status.value
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_type_ = account_type
        self.allowed_scopes_ = allowed_scopes
        self.redirect_uri = redirect_uri

    @property
    def client_type(self):
        return 'non-confidential'

    @property
    def status(self):
        return ClientStatus(self.status_)

    @property
    def account_type(self):
        return AccountType(self.account_type_)

    @property
    def redirect_uris(self):
        return [self.redirect_uri] if self.redirect_uri else []

    @property
    def default_redirect_uri(self):
        if self.redirect_uri:
            return self.redirect_uri

    @property
    def allowed_scopes(self):
        return [name for name in self.allowed_scopes_.split(',')]

    @property
    def default_scopes(self):
        return self.allowed_scopes if self.allowed_scopes else [OAuthScope.basic.name]

    @cached_property
    def user_class(self):
        from black_market.model.user.consts import AccountType
        from black_market.model.user.student import Student
        if self.account_type is AccountType.student:
            return Student
        raise ValueError

    def validate_scopes(self, scopes):
        return set(self.allowed_scopes).issuperset(set(scopes))

    @classmethod
    def add(cls, name, account_type, allowed_scopes=None, redirect_uri=''):
        client_id = generate_token()
        client_secret = generate_token()
        allowed_scopes = ','.join(scope.strip() for scope in allowed_scopes)

        oauth_client = OAuthClient(
            name, ClientStatus.normal, client_id, client_secret,
            account_type.value, allowed_scopes, redirect_uri)
        db.session.add(oauth_client)
        db.session.commit()
        return oauth_client.id

    def edit(self, new_name, new_redirect_uri):
        self.name = new_name
        self.redirect_uri = new_redirect_uri
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_client_id(cls, client_id):
        return cls.query.filter_by(client_id=client_id).first()

    def is_normal(self):
        return self.status is ClientStatus.normal

    def is_banned(self):
        return self.status is ClientStatus.banned

    def to_normal(self):
        self._update_status(ClientStatus.normal)

    def to_banned(self):
        self._update_status(ClientStatus.banned)

    def _update_status(self, status):
        self.status = status.value
        db.session.add(self)
        db.session.commit()
