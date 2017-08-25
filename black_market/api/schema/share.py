from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class SharePostSchema(BaseSchema, FillHelperMixin):
    post_id = ma.String(required=True)
    post_type = ma.Integer(required=True)
    student_id = ma.Integer()
