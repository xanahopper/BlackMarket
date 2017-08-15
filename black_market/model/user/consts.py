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


class UserBehaviorType(Enum):
    view_course_post = 0
    create_course_post = 1
    edit_course_post = 2
    markdone_course_post = 3
    view_goods_post = 5
    create_goods_post = 6
    edit_goods_post = 7
    markdone_goods_post = 8
    view_other_profile = 9
    view_other_posts = 10


MIN_PASSWD_LEN = 6
MAX_PASSWD_LEN = 20
