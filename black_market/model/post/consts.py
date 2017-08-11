from enum import Enum


class PostStatus(Enum):
    normal = 0
    succeed = 1
    abandoned = 2


class PostMobileSwitch(Enum):
    off = 0     # not display mobile
    on = 1      # display mobile
