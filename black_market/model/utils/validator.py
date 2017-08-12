import re
import decimal
from black_market.model.exceptions import (
    EmailFormatError,
    MobileFormatError, PasswordFormatError,
    NumberRangeError, InvalidValueError, NameFormatError
)
from black_market.model.user.consts import MIN_PASSWD_LEN, MAX_PASSWD_LEN

_WORD_RE = re.compile(r'^[a-zA-Z]+$')
_EMAIL_RE = re.compile(
    r'^[_\.0-9a-zA-Z+-]+@([0-9a-zA-Z]+[0-9a-zA-Z-]*\.)+[a-zA-Z]{2,4}$')
_PASSWORD_RE = re.compile(
    r'^[0-9a-zA-Z\~\)\!\$\%\*\(\_\+\-'
    "\=\{\}\[\]\|\:\;\<\>\,\.\/\@\#\^\&\"\'\`\?]+$")
_ZH_NAME = re.compile(r'[\u4e00-\u9fa5]{2,20}$')
_EN_NAME = re.compile(r'[a-zA-Z ]{2,20}$')

_URL_RE = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)


# 驰声科技跟读文本表达式：限定40个单词。目前只支持单个数字［0-9]。并且单个数字就是独立单词
# www.chivox.com
_CHIVOX_TEXT_RE = re.compile(r'^((([A-Za-z.\'\"]+[,.:!?\"]{0,2})|([0-9]{1})) ){0,39}'
                             r'(([A-Za-z.\'\"]+[,.:!?\"]{0,2})|([0-9]{1}))$')

_POINTS_RE = re.compile(r'^\d{1,4}$|^\d{1,4}\.\d$')


def validate_email(value):
    email = value
    if not email or not len(email) >= 6 or not _EMAIL_RE.match(email):
        raise EmailFormatError
    return True


def validate_phone(value):
    phone_number = value
    if not phone_number:
        raise MobileFormatError('请输入正确的手机号')
    p = re.compile(r'^1[3|4|5|8|7]\d{9}$')
    m = p.match(phone_number)
    if m:
        return True
    raise MobileFormatError('请输入正确的手机号')


def validate_password(value):
    password = value
    if not password:
        raise MobileFormatError
    elif not (MIN_PASSWD_LEN <= len(password) <= MAX_PASSWD_LEN):
        raise PasswordFormatError
    if not _PASSWORD_RE.match(password):
        raise PasswordFormatError
    return True


def validate_enum(value, enum_cls):
    try:
        return enum_cls(int(value))
    except (TypeError, ValueError):
        raise InvalidValueError('Invalid value {value} for {enum}'.format(
            value=value, enum=enum_cls.__name__))


def validate_zh_name(value):
    zh_name = value
    if not zh_name:
        raise NameFormatError
    if not _ZH_NAME.match(zh_name):
        raise NameFormatError
    return True


def validate_en_name(value):
    en_name = value
    if not en_name:
        raise NameFormatError('请正确输入英文名，2-20个英文字母')
    if not _EN_NAME.match(en_name):
        raise NameFormatError('请正确输入英文名，2-20个英文字母')
    return True


def validate_len(text, min_len, max_len):
    assert isinstance(min_len, int)
    assert isinstance(max_len, int)
    assert max_len >= min_len

    tlen = len(text)
    validate_number_range(tlen, min_len, max_len)


def validate_number_range(value, min_value=None, max_value=None):
    assert isinstance(value, (int, decimal.Decimal))
    if min_value is None and max_value is None:
        return value
    elif min_value is None and max_value is not None:
        if value > max_value:
            raise NumberRangeError()
    elif min_value is not None and max_value is None:
        if value < min_value:
            raise NumberRangeError()
    else:
        if not min_value <= value <= max_value:
            raise NumberRangeError()
