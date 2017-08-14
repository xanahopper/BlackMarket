from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class CreateStudentSchema(BaseSchema, FillHelperMixin):
    mobile = ma.String(required=True)
    type = ma.Integer(required=True)
    grade = ma.String(required=True)
    verify_code = ma.String(required=True)


class RegisterStudentSchema(BaseSchema, FillHelperMixin):
    mobile = ma.String(required=True)


class UpdateStudentSchema(BaseSchema, FillHelperMixin):
    type = ma.Integer(required=True)
    grade = ma.String(required=True)


class GetMyCoursePostSchema(BaseSchema, FillHelperMixin):
    start = ma.Integer()
    limit = ma.Integer()
    order = ma.Integer()
