from black_market.ext import ma

from .base import BaseSchema, FillHelperMixin


class GetUploadTokenSchema(BaseSchema, FillHelperMixin):
    ext = ma.String(required=True)
