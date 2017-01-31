import re
import datetime

from flask import flash, redirect

from black_market.models.models import User


def timestamp_to_datetime(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime("%Y-%m-%d %H:%M:%S")


def redirect_with_msg(target, msg, category):
    if not msg:
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
