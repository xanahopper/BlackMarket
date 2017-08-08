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


class TeacherHasClassChangeSchoolError(BlackMarketError):
    _error = Error(405, '老师要换学校，这个老师必须没有班级！', 403)


class TeacherAlreadyBoundWeixinError(BlackMarketError):
    _error = Error(406, '教师手机号账号已绑定过微信', 403)


class TeacherAccountUncreatedError(BlackMarketError):
    _error = Error(407, '您的手机号没有被市场人员录入开通，请致电：15321563358', 403)


class EmailAlreadyExistedError(BlackMarketError):
    _error = Error(408, '邮箱已存在', 403)


class WeixinAlreadyExistedError(BlackMarketError):
    _error = Error(409, '微信已存在', 403)


# 学校班级类错误(500~599)
class ClassTooManyStudentError(BlackMarketError):
    _error = Error(500, '一个班的学生已经达到上限了！', 403)


# 代理商代表类错误(600~699)
class AgentHasSchoolChangeLocationError(BlackMarketError):
    _error = Error(600, '代理代表要换地区，这个地区的学校必须找到新的代理代表！', 403)


# 广告类错误(700~749)
class AdShelvingConflictError(BlackMarketError):
    _error = Error(700, '已有广告正在使用中，请关闭后发布新广告', 403)


class AdShelvingChangeError(BlackMarketError):
    _error = Error(701, '广告上下架失败，请重新操作', 403)


# 有声书类错误(750~849)
class AudiobookRecordOverLimitError(BlackMarketError):
    _error = Error(750, '此绘本录制保存的空间已满，请先删除一些再录制', 403)


class AudiobookNotFoundError(BlackMarketError):
    _error = Error(751, '有声绘本可能已被删除，请重新进入绘本录制查看。', 404)


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
