from functools import update_wrapper

from flask import request, g

from black_market.model.wechat.session import WechatSession
from black_market.model.exceptions import (
    MissingSessionKeyError, InvalidSessionKeyError, WechatUserNotFoundError)
from black_market.config import DISABLE_SESSION_CHECK


def require_session_key(require_wechat_user=True):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):

            # TODO remove this later
            if DISABLE_SESSION_CHECK:
                return wrapped(*args, **kwargs)

            session_key = request.headers.get('X-User-Session-Key', '')

            if not session_key:
                raise MissingSessionKeyError()

            wechat_session = WechatSession.get_by_third_session_key(session_key)

            if not wechat_session:
                raise InvalidSessionKeyError()

            wechat_user = wechat_session.wechat_user

            if require_wechat_user:
                if not wechat_user:
                    raise WechatUserNotFoundError()

            g.wechat_session = wechat_session
            g.wechat_user = wechat_user

            return wrapped(*args, **kwargs)
        return update_wrapper(wrapper, wrapped)
    return decorator
