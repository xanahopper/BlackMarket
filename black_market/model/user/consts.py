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
    create_account = 1
    edit_profile = 2

    view_course_post = 3
    view_course_post_contact = 4
    create_course_post = 5
    edit_course_post = 6
    markdone_course_post = 7
    share_course_post = 8

    view_goods_post = 9
    view_goods_post_contact = 10
    create_goods_post = 11
    edit_goods_post = 12
    markdone_goods_post = 13
    share_goods_post = 14

    view_other_profile = 15
    view_other_posts = 16
    upload_photo = 17


MIN_PASSWD_LEN = 6
MAX_PASSWD_LEN = 20
