from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


# TODO
class UpdateWechatUserSchema(BaseSchema, FillHelperMixin):
    userInfo = ma.String(required=True)
    nickName = ma.Integer(required=True)
    gender = ma.String(required=True)
    language = ma.String(required=True)
    city = ma.String(required=True)
    province = ma.String(required=True)
    country = ma.String(required=True)
    avatarUrl = ma.String(required=True)
