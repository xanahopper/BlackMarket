from functools import update_wrapper

from flask import request, abort, jsonify

from black_market.ext import oauth_server
from black_market.model.oauth.client import OAuthClient
from black_market.model.oauth.scopes import OAuthScope


def require_credentials(scopes=None):
    """A decorator to restrict views to be accessible with client credentials.

    This is usually used in anonymous API.
    """

    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            client_id = request.headers.get('X-Client-ID', '')

            if not client_id:
                return jsonify(error='missing_token'), 401

            client = OAuthClient.get_by_client_id(client_id)
            if not client:
                return jsonify(error='invalid_token'), 403

            # TODO client.allowed_scopes should be [Enum, Enum, ...]
            # if scopes and not any(s for s in client.c if s in scopes):
            #     return jsonify(error='invalid_scope'), 403

            request.oauth_client = client
            return wrapped(*args, **kwargs)
        return update_wrapper(wrapper, wrapped)
    return decorator


def require_oauth(scopes):
    """A decorator to restrict views to be accessible with authorized user."""
    scopes = [OAuthScope(scope).name for scope in scopes]
    decorator = oauth_server.require_oauth(*scopes)

    def secondary_decorator(wrapped):
        def wrapper(*args, **kwargs):
            if 0:
                # TODO: Prevents dangerous usage when debugging
                if any([
                    ('X-Client-ID' in request.headers),
                    ('X-Client-Secret' in request.headers),
                    ('token' in request.values),
                ]):
                    abort(400, u'The client credentials should be excluded '
                               u'from this kind of request')
            return decorator(wrapped)(*args, **kwargs)
        return update_wrapper(wrapper, wrapped)
    return secondary_decorator
