from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class SharePostSchema(BaseSchema, FillHelperMixin):
    post_id = ma.Integer(required=True)
    post_type = ma.Integer(required=True)
    student_id = ma.Integer()


class ShareMeSchema(BaseSchema, FillHelperMixin):
    student_id = ma.Integer(required=True)
