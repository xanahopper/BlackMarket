from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class CreateStudentSchema(BaseSchema, FillHelperMixin):
    mobile = ma.String(required=True)
    raw_password = ma.String(required=True)
    password_repeat = ma.String(required=True)
    name = ma.String(required=True)
    gender = ma.Integer(required=True)
    type = ma.Integer(required=True)
    grade = ma.String(required=True)
    verify_code = ma.String(required=True)