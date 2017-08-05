from datetime import datetime, timedelta

from arrow import Arrow
from werkzeug.utils import cached_property

from black_market.config import OAUTH_TOKEN_TTL
from black_market.ext import db
from black_market.libs.cache.redis import mc
from .client import OAuthClient


class OAuthToken(db.Model):
    __tablename__ = 'oauth_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_pk = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    access_token = db.Column(db.String(80))
    refresh_token = db.Column(db.String(80))
    scopes_ = db.Column(db.String(80))
    expires_in = db.Column(db.Integer)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)

    _cache_key_prefix = 'oauth_token:'
    _token_cache_key = _cache_key_prefix + 'id:%s'
    _id_by_token_type_and_value_cache_key = _cache_key_prefix + 'type:%s:value:%s'
    _ids_by_user_id_cache_key = _cache_key_prefix + 'user.id:%s'

    def __init__(self, client_pk, user_id, scopes, access_token,
                 refresh_token, expires_in):
        # client_pk是client的id
        # refresh_token时Flask-OAuthlib会获取client_id比对，这里要区分一下
        self.client_pk = client_pk
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scopes_ = scopes
        self.expires_in = expires_in

    def dump(self):
        return dict(
            token_type='Bearer',
            scope=' '.join(self.scopes),
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            expires_in=self.expires_in
        )

    @property
    def scopes(self):
        return self.scopes_.split(',')

    @cached_property
    def client(self):
        return OAuthClient.get(self.client_pk)

    @cached_property
    def client_id(self):
        return self.client.client_id

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
    def user(self):
        return self.user_class.get(self.user_id)

    @cached_property
    def expires(self):
        creation_time = Arrow.fromdatetime(self.create_time, 'local')
        expires_delta = timedelta(seconds=self.expires_in)
        return (creation_time.to('utc') + expires_delta).naive

    @property
    def available(self):
        rest_lifetime = (self.expires - datetime.now()).seconds
        entire_lifetime = (self.expires - self.create_time).seconds
        return rest_lifetime / entire_lifetime > 0.3

    @classmethod
    def add(cls, client_pk, user_id, scopes, access_token, refresh_token,
            expires_in=OAUTH_TOKEN_TTL):
        scopes = ','.join(scope.strip() for scope in scopes)
        oauth_token = OAuthToken(client_pk, user_id, scopes, access_token, refresh_token, expires_in)
        db.session.add(oauth_token)
        db.session.commit()
        return oauth_token.id

    @classmethod
    def get(cls, id_):
        return OAuthToken.query.get(id_)

    @classmethod
    def get_by_token(cls, token_type, token):
        if token_type in ('access_token', 'refresh_token'):
            if token_type == 'access_token':
                return OAuthToken.query.filter_by(access_token=token).first()
            else:
                return OAuthToken.query.filter_by(refresh_token=token).first()

    @classmethod
    def get_by_access_token(cls, access_token):
        return cls.get_by_token('access_token', access_token)

    @classmethod
    def get_by_refresh_token(cls, refresh_token):
        return cls.get_by_token('refresh_token', refresh_token)

    @classmethod
    def gets_by_user_id(cls, user_id):
        return OAuthToken.query.filter_by(user_id=user_id).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        self.clear_cache()

    def clear_cache(self):
        mc.delete(self._token_cache_key % self.id)
        mc.delete(self._id_by_token_type_and_value_cache_key % (
            'access_token', self.access_token))
        mc.delete(self._id_by_token_type_and_value_cache_key % (
            'refresh_token', self.refresh_token))
        mc.delete(self._ids_by_user_id_cache_key % self.user_id)


def delete_oauth_tokens(user_id):
    tokens = OAuthToken.gets_by_user_id(user_id)
    for token in tokens:
        token.delete()
