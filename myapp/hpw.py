import random
import string
import hashlib


# helper functions to hash passwords and validate hashed passwords
def make_salt(length=5):
    # py2 = string.letters / # py3 = string.ascii_letters
    return "".join(random.choice(string.letters) for x in range(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()

    h = name + pw + salt
    return '%s|%s' % (hashlib.sha256(h.encode('utf-8')).hexdigest(), salt)


def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)
