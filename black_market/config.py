from envcfg.json.black_market import DEBUG
from envcfg.json.black_market import HTTP_HOST
from envcfg.json.black_market import HTTP_PORT
from envcfg.json.black_market import DOMAIN
from envcfg.json.black_market import SECRET_KEY
from envcfg.json.black_market import SENTRY_DSN
from envcfg.json.black_market import MYSQL_DSN
from envcfg.json.black_market import SQLALCHEMY_ECHO
from envcfg.json.black_market import RAW_SALT
from envcfg.json.black_market import FERNET_KEY
from envcfg.json.black_market import OAUTH2_PROVIDER_TOKEN_EXPIRES_IN
from envcfg.json.black_market import SMS_YUNPIAN_HTTP
from envcfg.json.black_market import SMS_YUNPIAN_APIKEY
from envcfg.json.black_market import WEIXIN_APP_ID
from envcfg.json.black_market import WEIXIN_APP_SECRET
from envcfg.json.black_market import DISABLE_SESSION_CHECK
from envcfg.json.black_market import QINIU_ACCESS_KEY
from envcfg.json.black_market import QINIU_SECRET_KEY
from envcfg.json.black_market import QINIU_BUCKET
from envcfg.json.black_market import QINIU_DOMAIN


APP = 'black_market'

OAUTH_TOKEN_TTL = OAUTH2_PROVIDER_TOKEN_EXPIRES_IN


__all__ = [
    'APP',
    'DEBUG',
    'HTTP_HOST',
    'HTTP_PORT',
    'DOMAIN',
    'SECRET_KEY',
    'SENTRY_DSN',
    'MYSQL_DSN',
    'SQLALCHEMY_ECHO',
    'RAW_SALT',
    'FERNET_KEY',
    'OAUTH_TOKEN_TTL',
    'SMS_YUNPIAN_HTTP',
    'SMS_YUNPIAN_APIKEY',
    'WEIXIN_APP_ID',
    'WEIXIN_APP_SECRET',
    'DISABLE_SESSION_CHECK',
    'QINIU_ACCESS_KEY',
    'QINIU_SECRET_KEY',
    'QINIU_BUCKET',
    'QINIU_DOMAIN',
]
