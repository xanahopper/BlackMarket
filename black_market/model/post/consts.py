from enum import Enum


class PostStatus(Enum):
    normal = 0
    succeed = 1
    abandoned = 2


class PostMobileSwitch(Enum):
    off = 0     # not display mobile
    on = 1      # display mobile


class OrderType(Enum):
    descending = 0
    ascending = 1


class PostType(Enum):
    course_post = 1
    goods_post = 2
