from .base import BaseTestCase
import pytest

from black_market.model.code.verify import SMSVerify
from black_market.model.code.consts import SMSVerifyType
from black_market.libs.cache.redis import rd
from black_market.model.exceptions import SendSMSTooManyTimesError
from black_market.model.exceptions import AtemptTooManyTimesError


class VerifyCodeTest(BaseTestCase):

    def test_verify(self):
        mobile = '13600000000'
        type_ = SMSVerifyType.register
        v = SMSVerify.add(mobile, type_)
        assert v
        redis_key = SMSVerify._redis_key.format(mobile=mobile, type_=type_.value)
        assert v == rd.get(redis_key)
        assert SMSVerify.verify(mobile, v, type_)

    def test_verify_retry(self):
        mobile = '13600000000'
        type_ = SMSVerifyType.register
        v = SMSVerify.add(mobile, type_)
        assert v
        redis_key = SMSVerify._redis_key.format(mobile=mobile, type_=type_.value)
        assert v == rd.get(redis_key)
        for i in range(5):
            assert not SMSVerify.verify(mobile, v + '1', type_)
        with pytest.raises(AtemptTooManyTimesError):
            SMSVerify.verify(mobile, v + '1', type_)

    def test_send_too_many_times(self):
        mobile = '13600000000'
        type_ = SMSVerifyType.register
        for i in range(5):
            SMSVerify.add(mobile, type_)
        with pytest.raises(SendSMSTooManyTimesError):
            SMSVerify.add(mobile, type_)
