import re
import datetime

from flask import flash, redirect

from black_market.models.models import User


def timestamp_to_datetime(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime("%Y-%m-%d %H:%M:%S")


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
