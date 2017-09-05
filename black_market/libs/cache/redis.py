import redis

mc = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
rd = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)
rd2 = redis.StrictRedis(host='localhost', port=6379, db=2, decode_responses=True)

ONE_MINUTE = 60
HALF_HOUR = 1800
ONE_HOUR = 3600
HALF_DAY = ONE_HOUR * 12
ONE_DAY = ONE_HOUR * 24
ONE_WEEK = ONE_DAY * 7
ONE_MONTH = ONE_DAY * 30
ONE_YEAR = ONE_DAY * 365
