from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class SharePostSchema(BaseSchema, FillHelperMixin):
    post_id = ma.Integer(required=True)
    post_type = ma.Integer(required=True)
    student_id = ma.Integer()


class ShareStudentSchema(BaseSchema, FillHelperMixin):
    student_id = ma.Integer(required=True)


class GetShareStudentImageSchema(BaseSchema, FillHelperMixin):
    path = ma.String()


class GetSharePostImageSchema(BaseSchema, FillHelperMixin):
    path = ma.String()
    supply = ma.String()
    demand = ma.String()
    student_id = ma.String()
