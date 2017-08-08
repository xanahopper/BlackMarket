from enum import Enum


class AccountStatus(Enum):
    normal = 0
    need_verify = 1
    banned = 2


class Gender(Enum):
    unknown = 0
    male = 1
    female = 2


class StudentType(Enum):
    other = 0
    double_major = 1
    ppe = 2

MIN_PASSWD_LEN = 6
MAX_PASSWD_LEN = 20
