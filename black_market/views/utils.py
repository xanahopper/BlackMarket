import datetime
import random

from flask import flash, redirect, jsonify


def normal_jsonify(data, code=0, message=None):
    return jsonify(code=code, message=message, data=data), 200


def timestamp_to_datetime(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime("%Y-%m-%d %H:%M:%S")


def num_to_word(day):
    d = {1: '周一', 2: '周二', 3: '周三', 4: '周四',
         5: '周五', 6: '周六', 7: '周日'}
    return d.get(int(day))


def parse_contact(contact, phone):
    if phone not in contact:
        return contact
    d = {0: '零', 1: '壹', 2: '贰', 3: '叁', 4: '肆',
         5: '伍', 6: '陆', 7: '柒', 8: '捌', 9: '玖'}
    s = ''
    nums = random.sample(
        [i for i in range(0, len(phone))], int(len(phone) / 2))
    for i in phone:
        s = s + d.get(int(i)) if int(i) in nums else s + i
    return contact.replace(phone, s)


def flash_form_data(phone=None, username=None, email=None, message=None):
    if phone:
        flash(phone, category='phone')
    if username:
        flash(username, category='username')
    if email:
        flash(email, category='email')
    if message:
        flash(message, category='message')


def redirect_with_msg(target, msg, category):
    if msg:
        flash(msg, category=category)
    return redirect(target)


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


def get_short_message(message):
    max_len = 18
    return message[:max_len] + '...' if len(message) > max_len else message
