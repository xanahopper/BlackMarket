from envcfg.json.black_market import CELERY_BROKER_URL
from envcfg.json.black_market import CELERY_RESULT_BACKEND

from tzlocal import get_localzone

CELERY_TIMEZONE = get_localzone().zone

BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND

CELERY_INCLUDE = ('black_market.model.user.student',)
