import random
import hashlib

from black_market.config import RAW_SALT


def gen_salt(raw_salt=RAW_SALT):
    return '.'.join(random.sample(raw_salt, 10))


def hash_password(password, salt):
    m = hashlib.md5()
    m.update((password + salt).encode('utf-8'))
    password = m.hexdigest()
    return password
