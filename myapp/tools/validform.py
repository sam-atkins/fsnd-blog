"""
Validates user registration using Regex to check
for common issues with usernames, passwords and emails
"""

import re


# Regex for form error handling
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_PW = re.compile(r"^.{3,20}$")
USER_EM = re.compile(r"^[\S]+@[\S]+.[\S]+$")


# helper functions for Signup Handler
def valid_username(username):
    """Validates username against regex statement"""
    return username and USER_RE.match(username)


def valid_password(password):
    """Validates password against regex statement"""
    return password and USER_RE.match(password)


def valid_email(email):
    """Validates email against regex statement"""
    return not email or USER_EM.match(email)
