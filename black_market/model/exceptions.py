from collections import namedtuple


Error = namedtuple('Error', ['code', 'message', 'http_status_code'])


class BlackMarketError(Exception):
    """BlackMarket Base Exception"""
    _error = Error(0, '未知错误，请重试', 403)
    sentry_warning = False

    def __init__(self, message=''):
        super(BlackMarketError, self).__init__(message)
        self.message = message or self._error.message
        self.code = self._error.code
        self.http_status_code = self._error.http_status_code


#: 基础类错误(1 ~ 99)
class InvalidValueError(BlackMarketError):
    _error = Error(1, '请求参数不正确', 400)


class InvalidSMSVerifyCodeError(BlackMarketError):
    _error = Error(11, '请输入正确的短信验证码', 403)


class OAuthClientError(BlackMarketError):
    _error = Error(12, 'OAuth客户端错误', 403)
    sentry_warning = True


class InvalidCaptchaError(BlackMarketError):
    _error = Error(13, '请输入正确的图片验证码', 403)


class CaptchaVerifyRequiredError(BlackMarketError):
    _error = Error(14, '需要图片验证码', 400)


class EmailFormatError(BlackMarketError):
    _error = Error(16, 'Email格式错误', 400)


class MobileFormatError(BlackMarketError):
    _error = Error(17, '手机号格式错误', 400)


class PasswordFormatError(BlackMarketError):
    _error = Error(18, '请输入6-20位密码，不能包含空格', 400)


class UrlFormatError(BlackMarketError):
    _error = Error(19, 'URL格式错误', 400)


class NumberRangeError(BlackMarketError):
    _error = Error(20, '数字/长度不符合区间要求', 400)


class InvalidDatetimeError(BlackMarketError):
    _error = Error(21, '日期时间格式错误', 400)


class NameAlreadyExistedError(BlackMarketError):
    _error = Error(22, '名称重复', 400)


class URLFormatError(BlackMarketError):
    _error = Error(23, 'URL格式错误(确保http(s)://开头且20-255字符)', 400)


class URLUnreachableError(BlackMarketError):
    _error = Error(24, 'URL无法访问，请确认是否填写正确', 400)


#: 账号类(400~499)
class MobileAlreadyExistedError(BlackMarketError):
    _error = Error(400, '手机号已存在', 403)


class NameFormatError(BlackMarketError):
    _error = Error(401, '请正确输⼊姓名，2-10个汉字', 400)


class AliasAlreadyExistedError(BlackMarketError):
    _error = Error(402, '账号已经存在', 403)


class UserNotFoundError(BlackMarketError):
    _error = Error(403, '用户不存在', 404)


class IncorrectPasswordError(BlackMarketError):
    _error = Error(404, '密码错误', 400)


class EmailAlreadyExistedError(BlackMarketError):
    _error = Error(405, '邮箱已存在', 403)


class WeixinAlreadyExistedError(BlackMarketError):
    _error = Error(406, '微信已存在', 403)


class SupplySameAsDemandError(BlackMarketError):
    _error = Error(407, '供给与需求不可以相同', 403)


class InvalidPostError(BlackMarketError):
    _error = Error(408, '无效的Post，请重新检查填写的信息', 403)


# 反馈类错误(850~599)
class FeedbackTooLongError(BlackMarketError):
    _error = Error(850, '描述超过1000字，请重新编辑', 400)


# 请求 limit 之类的错误
class SendSMSTooManyTimesError(BlackMarketError):
    _error = Error(995, '已超出当日获取验证码最大次数，请24小时后重试', 429)


class LoginTooManyTimesError(BlackMarketError):
    _error = Error(996, '尝试登陆次数太多', 429)


class AtemptTooManyTimesError(BlackMarketError):
    _error = Error(997, '尝试次数太多', 429)


class RequestFailedError(BlackMarketError):
    _error = Error(998, 'Parameters were valid but the request failed.', 402)


class LockError(BlackMarketError):
    _error = Error(999, '操作太快了！', 429)


class RequestTooFrequentError(BlackMarketError):
    _error = Error(1000, '您的操作太过频繁，请稍后重试', 429)


class RetryError(BlackMarketError):
    _error = Error(1500, 'Need retry somehow', 402)


# 第三方服务异常
class WeChatServiceError(BlackMarketError):
    _error = Error(4000, '微信服务异常', 403)


class WechatUserNotExistedError(BlackMarketError):
    _error = Error(4001, '微信服务异常', 403)
