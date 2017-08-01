import flask
from black_market.ext import ma


class FillHelperMixin(object):

    def fill(self, src=None, extra=None):
        request = flask.request
        if src is None:
            if request.method in ('POST', 'PUT', 'PATCH'):
                src = 'form'
            elif request.method in ('GET', 'HEAD', 'DELETE'):
                src = 'query'
            else:
                raise ValueError('Unknown method {}'.format(request.method))
        assert src in ('form', 'query', 'both')
        if src == 'form':
            if request.mimetype != 'application/json':
                flask.abort(400)
            payload = request.get_json()
        elif src == 'query':
            payload = request.args.to_dict()
        elif src == 'both':
            payload = request.values.to_dict()

        if extra:
            payload.update(extra)

        return self.load(payload).data


class BaseSchema(ma.Schema):

    class Meta:
        strict = True

    def load_and_dump(self, src):
        mid = self.load(src).data
        return self.dump(mid).data
