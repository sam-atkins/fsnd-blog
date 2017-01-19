"""
Makes and checks secure hashed strings
for use as cookies to enable usernames
"""

import hashlib
import hmac
import myapp.secret_stuff


def hash_str(name):
    """Hashes the var name along with a secret string"""
    return hmac.new(myapp.secret_stuff.SECRET,
                    name.encode('utf-8'), hashlib.md5).hexdigest()


def make_secure_val(name):
    """Combines string name with a hash, separated by | """
    h_name = hash_str(name)
    return name + "|" + h_name


def check_secure_val(h_name):
    """checks the secure value, splitting the username before | and
    the hashed string after"""
    val = h_name.split('|')[0]
    if h_name == make_secure_val(val):
        return val
