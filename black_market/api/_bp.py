from flask import Blueprint


def create_blueprint(name, version, package_name, **kwargs):
    url_prefix = kwargs.pop('url_prefix', '/{}'.format(name))
    url_prefix = '/api/{version}{url_prefix}'.format(
        version=version, url_prefix=url_prefix)
    bp_name = '{name}'.format(name=name)
    bp = Blueprint(bp_name, package_name, url_prefix=url_prefix, **kwargs)
    return bp
