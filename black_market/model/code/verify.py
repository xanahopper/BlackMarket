import random
import string
from black_market.libs.cache.redis import rd, ONE_DAY
# from black_market.model.exceptions import AtemptTooManyTimesError
# from black_market.model.exceptions import SendSMSTooManyTimesError


class SMSVerify(object):
    _redis_key = 'sms:verify:{type_}:{mobile}'
    _total_retry_key = 'sms:verify:{type_}:{mobile}:retry.total'
    _total_send_key = 'sms:verify:{type_}:{mobile}:send.total'
    _expire_time = 60 * 10  # 10 mins

    @classmethod
    def add(cls, mobile, type_, max_send_total=5):
        total_send_key = cls._total_send_key.format(mobile=mobile, type_=type_.value)
        total_send = int(rd.get(total_send_key)) if rd.get(total_send_key) else 0
        # if total_send and total_send >= max_send_total:
        #     raise SendSMSTooManyTimesError(
        #         '已超出当日最大获取验证码次数，请24小时后尝试')

        code = cls._gen_verify_code()
        key = cls._redis_key.format(mobile=mobile, type_=type_.value)
        existed = rd.get(key)
        if existed:
            rd.delete(key)
        rd.set(key, code)
        rd.expire(key, cls._expire_time)

        rd.incr(total_send_key)
        if not total_send:
            rd.expire(total_send_key, ONE_DAY)
        return code

    @classmethod
    def verify(cls, mobile, code, type_, max_retry=5):
        key = cls._redis_key.format(mobile=mobile, type_=type_.value)
        total_retry_key = cls._total_retry_key.format(mobile=mobile, type_=type_.value)
        # retry_total = int(rd.get(total_retry_key)) if rd.get(total_retry_key) else 0
        # if retry_total >= max_retry:
        #     rd.delete(key)
        #     rd.delete(total_retry_key)
        #     raise AtemptTooManyTimesError('验证码错误输入次数过多，请重新获取')
        cached_code = rd.get(key)
        if cached_code == str(code):
            rd.delete(key)
            rd.delete(total_retry_key)
            return True
        rd.incr(total_retry_key)
        return False

    @classmethod
    def _gen_verify_code(cls, length=6):
        return ''.join(random.choice(string.digits) for _ in range(length))
