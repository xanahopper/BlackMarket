from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class CreateCoursePostSchema(BaseSchema, FillHelperMixin):
    student_id = ma.String(required=True)
    switch = ma.Integer(required=True)
    mobile = ma.String(required=True)
    wechat = ma.String(required=True)
    message = ma.String(required=True)


class UpdateCoursePostSchema(BaseSchema, FillHelperMixin):
    message = ma.String()
    status = ma.Integer()


class GetCoursePostSchema(BaseSchema, FillHelperMixin):
    start = ma.Integer(required=True)
    limit = ma.Integer(required=True)
