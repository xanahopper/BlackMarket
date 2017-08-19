from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class GetUploadTokenSchema(BaseSchema, FillHelperMixin):
    ext = ma.String(required=True)


class QiniuCallbackSchema(BaseSchema, FillHelperMixin):
    key = ma.String(required=True)
    filesize = ma.String(required=True)
    hash = ma.String(required=True)
