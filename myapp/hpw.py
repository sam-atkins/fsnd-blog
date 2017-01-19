"""
Hashes passwords for storage in ndb
Includes funcs to make a random salt, hash a password,
and validate an existing password
"""

import random
import string
import hashlib


# helper functions to hash passwords and validate hashed passwords
def make_salt(length=5):
    """Makes a random salt at length = x"""
    # py2 = string.letters / # py3 = string.ascii_letters
    return "".join(random.choice(string.letters) for x in range(length))


def make_pw_hash(name, pword, salt=None):
    """Hashes a password to save in ndb"""
    if not salt:
        salt = make_salt()

    h_pw = name + pword + salt
    return '%s|%s' % (hashlib.sha256(h_pw.encode('utf-8')).hexdigest(), salt)


def valid_pw(name, pword, h_val):
    """Validates a password is correct"""
    salt = h_val.split('|')[1]
    return h_val == make_pw_hash(name, pword, salt)
