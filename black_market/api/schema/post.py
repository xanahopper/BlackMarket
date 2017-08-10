from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class CreateCoursePostSchema(BaseSchema, FillHelperMixin):
    student_id = ma.String(required=True)
    contact = ma.Integer(required=True)
    message = ma.String(required=True)


class UpdateCoursePostSchema(BaseSchema, FillHelperMixin):
    contact = ma.Integer()
    message = ma.String()
    status = ma.Integer()


class GetCoursePostSchema(BaseSchema, FillHelperMixin):
    start = ma.Integer(required=True)
    limit = ma.Integer(required=True)
