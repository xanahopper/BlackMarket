from functools import update_wrapper

from flask import request, jsonify

from black_market.model.wechat.session import WechatSession


def require_session_key(require_wechat_user=True):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            session_key = request.headers.get('X-User-Session-Key', '')

            if not session_key:
                return jsonify(error='missing session key'), 401

            wechat_session = WechatSession.get_by_third_session_key(session_key)
            wechat_user = wechat_session.wechat_user

            if require_wechat_user:
                if not wechat_user:
                    return jsonify(error='wechat user does not exist'), 401

            request.wechat_session = wechat_session
            request.wechat_user = wechat_user

            return wrapped(*args, **kwargs)
        return update_wrapper(wrapper, wrapped)
    return decorator
