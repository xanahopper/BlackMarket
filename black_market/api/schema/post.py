from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class CreateCoursePostSchema(BaseSchema, FillHelperMixin):
    student_id = ma.String(required=True)
    switch = ma.Integer(required=True)
    mobile = ma.String(required=True)
    message = ma.String(required=True)
    wechat = ma.String()
    supply = ma.Integer()
    demand = ma.Integer()


class UpdateCoursePostSchema(BaseSchema, FillHelperMixin):
    message = ma.String()
    switch = ma.Integer()
    wechat = ma.String()


class UpdateCoursePostStatusSchema(BaseSchema, FillHelperMixin):
    status = ma.Integer(required=True)


class GetCoursePostSchema(BaseSchema, FillHelperMixin):
    start = ma.Integer()
    limit = ma.Integer()
    order = ma.Integer()
    supply = ma.Integer()
    demand = ma.Integer()
    closed = ma.Integer()


class DecrRemainingViewCountSchema(BaseSchema, FillHelperMixin):
    post_id = ma.Integer(required=True)


class CreateGoodsPostSchema(BaseSchema, FillHelperMixin):
    student_id = ma.String(required=True)
    switch = ma.Integer(required=True)
    mobile = ma.String(required=True)
    message = ma.String(required=True)
    wechat = ma.String()


class UpdateGoodsPostSchema(BaseSchema, FillHelperMixin):
    message = ma.String()
    switch = ma.Integer()
    wechat = ma.String()


class UpdateGoodsPostStatusSchema(BaseSchema, FillHelperMixin):
    status = ma.Integer(required=True)


class GetGoodsPostSchema(BaseSchema, FillHelperMixin):
    start = ma.Integer()
    limit = ma.Integer()
    order = ma.Integer()
    closed = ma.Integer()
