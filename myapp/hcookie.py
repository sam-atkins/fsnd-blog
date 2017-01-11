import hashlib
import hmac
import secret_stuff


def hash_str(s):
    return hmac.new(secret_stuff.SECRET,
                    s.encode('utf-8'), hashlib.md5).hexdigest()


def make_secure_val(s):
    h = hash_str(s)
    return s + "|" + h


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val
