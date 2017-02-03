import re
import datetime
import random

from flask import flash, redirect

from black_market.models.models import User


def timestamp_to_datetime(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime("%Y-%m-%d %H:%M:%S")


def num_to_word(day):
    d = {1: '周一', 2: '周二', 3: '周三', 4: '周四',
         5: '周五', 6: '周六', 7: '周日'}
    return d.get(int(day))


def get_phone_words(phone):
    d = {0: '零', 1: '壹', 2: '贰', 3: '叁', 4: '肆',
         5: '伍', 6: '陆', 7: '柒', 8: '捌', 9: '玖'}
    s = ''
    nums = random.sample([i for i in range(0, 10)], 5)
    for i in phone:
        s = s + d.get(int(i)) if int(i) in nums else s + i
    return s


def redirect_with_msg(target, msg, category):
    if msg:
        flash(msg, category=category)
    return redirect(target)


def check_phone(phone):
    pattern = re.compile(u'0?(13|14|15|17|18)[0-9]{9}')
    return bool(pattern.match(phone))


def check_email(email):
    pattern = re.compile(
        '\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
    return bool(pattern.match(email))


def check_exist(phone):
    return bool(User.query.filter_by(phone=phone).first())


def get_paginate_from_list(target, page, per_page):
    has_next = False
    start = per_page * (page - 1)
    end = per_page * page
    if len(target) <= start:
        return target, has_next
    elif len(target) <= end:
        return target[start:], has_next
    else:
        has_next = True
        return target[start:end], has_next
