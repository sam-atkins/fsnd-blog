"""
Decorators for validating if
- post exists
"""

# [START Imports]
from functools import wraps
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
from google.appengine.ext import ndb
# [END Imports]


def user_logged_in(function):
    """Validates if a user is logged in, if not
    redirect to login page
    """
    @wraps(function)
    def wrapper(self, *args):
        user = self.request.cookies.get('name')
        if user:
            return function(self, *args)
        else:
            self.redirect('/login')
            return
    return wrapper


def post_exists(function):
    """Validates if a post exists using post_id
    If post exists returns the function with post_id and the post
    Else returns a 404 error"""
    @wraps(function)
    def wrapper(self, post_id):
        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()
        if post:
            return function(self, post_id, post)
        else:
            self.error(404)
            return
    return wrapper


def user_owns_post(function):
    """Validates if the user owns the post
    If yes, returns the id and key to enable form render, edit & delete
    If no, redirects to the home page
    """
    @wraps(function)
    def wrapper(self, post_id, post):
        # establish user
        u = self.request.cookies.get('name')
        user = check_secure_val(u)

        # get comment key to establish commentator
        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        # if user == commentator, return function
        if user == post.author:
            return function(self, post_id, post)
        # else redirect to ('/')
        else:
            self.redirect('/')
            return
    return wrapper


def comment_exists(function):
    """Validates if a comment exists using comments_id
    If post exists returns the function with comments_id and the comment
    Else returns a 404 error"""
    @wraps(function)
    def wrapper(self, comments_id):
        key = ndb.Key('Comments', int(comments_id))
        c = key.get()
        if c:
            return function(self, comments_id, c)
        else:
            self.error(404)
            return
    return wrapper


def user_owns_comment(function):
    """Validates if the user owns the comment
    If yes, returns the id and key to enable form render and edit
    If no, redirects to the home page
    """
    @wraps(function)
    def wrapper(self, comments_id, c):
        # establish user
        u = self.request.cookies.get('name')
        user = check_secure_val(u)

        # get comment key to establish commentator
        key = ndb.Key('Comments', int(comments_id))
        c = key.get()

        # if user == commentator, return function
        if user == c.commentator:
            return function(self, comments_id, c)
        # else redirect to ('/')
        else:
            self.redirect('/')
            return
    return wrapper
