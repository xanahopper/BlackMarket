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
    # NSD 本科生
    undergraduate = 1
    # NSD 双学位项目学生
    double_major = 2
    # 元培政经哲学生
    ppe = 3


class UserBehaviorType(Enum):
    create_account = 10
    edit_profile = 11
    share_me_to_friend = 12
    get_share_me_image = 13

    view_course_post = 20
    view_course_post_contact = 21
    create_course_post = 22
    edit_course_post = 23
    markdone_course_post = 24
    share_course_post = 25
    get_share_course_post_image = 26

    view_goods_post = 30
    view_goods_post_contact = 31
    create_goods_post = 32
    edit_goods_post = 33
    markdone_goods_post = 43
    share_goods_post = 35
    get_share_goods_post_image = 36

    view_other_profile = 40
    view_other_posts = 41

    upload_photo = 50


MIN_PASSWD_LEN = 6
MAX_PASSWD_LEN = 20
