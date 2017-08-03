from flask import g, request

from black_market.model.oauth.token import OAuthToken
from black_market.model.oauth.client import OAuthClient
from black_market.model.oauth.grant import OAuthGrant
from black_market.model.user.consts import AccountType, AliasType
from black_market.model.user.student import Student
from black_market.ext import oauth_server

from ._bp import create_blueprint


bp = create_blueprint('oauth', __name__, url_prefix='/oauth')


@bp.before_request
def _parse_source():
    source = request.headers.get('X-Black-Market-Source')
    g.source = source


@oauth_server.clientgetter
def load_client(client_id):
    client = OAuthClient.get_by_client_id(client_id)
    if client and client.is_normal():
        return client


@oauth_server.grantgetter
def load_grant(client_id, code):
    return OAuthGrant.get_by_code(client_id, code)


@oauth_server.grantsetter
def save_grant(client_id, code_response, request, *args, **kwargs):
    id_ = OAuthGrant.add(
        client_id=client_id,
        code=code_response['code'],
        redirect_uri=request.request_uri,
        scopes=request.scopes,
        user_id=request.oauth.user.id
    )
    return OAuthGrant.get(id_)


@oauth_server.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return OAuthToken.get_by_access_token(access_token)
    elif refresh_token:
        return OAuthToken.get_by_refresh_token(refresh_token)


@oauth_server.tokensetter
def save_token(token, request, *args, **kwargs):
    id_ = OAuthToken.add(
        client_pk=request.client.id,
        user_id=request.user.id,
        scopes=token['scope'].split(),
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        expires_in=token['expires_in']
    )
    return OAuthToken.get(id_)


@oauth_server.usergetter
def get_user(username, password, *args, **kwargs):
    # if request.client.account_type is AccountType.student:
    student = Student.get_by_alias_and_type(username, AliasType.mobile)
    if not student.verify_password(password):
        return None
    return student


@bp.route('/token', methods=['POST'])
@oauth_server.token_handler
def access_token(*args, **kwargs):
    return {}


@bp.route('/revoke', methods=['POST'])
@oauth_server.revoke_handler
def revoke_token():
    return {}
