from envcfg.json.black_market import DEBUG
from envcfg.json.black_market import HTTP_HOST
from envcfg.json.black_market import HTTP_PORT
from envcfg.json.black_market import SECRET_KEY
from envcfg.json.black_market import SENTRY_DSN
from envcfg.json.black_market import MYSQL_DSN
from envcfg.json.black_market import RAW_SALT
from envcfg.json.black_market import OAUTH2_PROVIDER_TOKEN_EXPIRES_IN
from envcfg.json.black_market import SMS_YUNPIAN_HTTP
from envcfg.json.black_market import SMS_YUNPIAN_APIKEY
from envcfg.json.black_market import WEIXIN_APP_ID
from envcfg.json.black_market import WEIXIN_APP_SECRET


APP = 'black_market'

OAUTH_TOKEN_TTL = OAUTH2_PROVIDER_TOKEN_EXPIRES_IN


__all__ = [
    'APP',
    'DEBUG',
    'HTTP_HOST',
    'HTTP_PORT',
    'SECRET_KEY',
    'SENTRY_DSN',
    'MYSQL_DSN',
    'RAW_SALT',
    'OAUTH_TOKEN_TTL',
    'SMS_YUNPIAN_HTTP',
    'SMS_YUNPIAN_APIKEY',
    'WEIXIN_APP_ID',
    'WEIXIN_APP_SECRET',
]