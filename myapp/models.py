from google.appengine.ext import ndb

from hpw import *


# [START GQL Blogposts datastore & entity types]
class Blogposts(ndb.Model):
    """
    Adds blogposts (title, blogPost content, author, created and last
    modified) entity data types to the App Engine database.
    The model class specifies the entity data types.
    (required=True) - constraint enforces posts to database
    must have this value.
    email value - optional so no required=True statement;
    and StringProperty type used as EmailProperty type is
    mandatory and if used throws an error if no email is entered
    by the user.
    """

    title = ndb.StringProperty(required=True)
    blogPost = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    author = ndb.StringProperty(required=True)
# [END GQL datastore & entity types]


# [START Comments Model]
class Comments(ndb.Model):
    """
    Model for representing blogpost comments, linked to the Blogpost
    Model via the post_id of the blogpost.
    """

    blogpost_id = ndb.IntegerProperty(required=True)
    comment = ndb.TextProperty(required=True)
    commentator = ndb.StringProperty(required=True)
    comment_date = ndb.DateTimeProperty(auto_now_add=True)

    # @classmethod
    # def _find_comment_id(cls, post_id, username):
    #     """returns the id of the blogpost's comment"""

    #     query = Comments.query().filter(
    #         Comments.blogpost_id == post_id).filter(
    #         Comments.commentator == username)
    #     comment_id = query.get()
    #     return comment_id
# [END Comments Model]


# [START Likes data Model]
class Likes(ndb.Model):
    blogpost_id = ndb.IntegerProperty(required=True)
    like_count = ndb.IntegerProperty(required=True)
    username = ndb.StringProperty(required=True)

    @classmethod
    def _check_like(cls, post_id, username):
        """
        Checks if a blogpost (via the post_id key) already
        has a like by the user"""

        q = Likes.query().filter(Likes.blogpost_id == post_id).filter(
            Likes.username == username).get()
        if q:
            return True

    @classmethod
    def _add_like(cls, blogpost_id, username):
        """Used to add or remove a like by a user against a blogpost (key)"""

        like_count = 1
        return Likes(blogpost_id=blogpost_id, like_count=like_count,
                     username=username)

    @classmethod
    def _find_like_key(cls, post_id, username):
        """returns the id of the blogpost's like which
        the user already liked previously"""

        query = Likes.query().filter(Likes.blogpost_id == post_id).filter(
            Likes.username == username)
        like_id = query.get()
        return like_id

    @classmethod
    def _subtract_like(cls, blogpost_id, username):
        """Used to add or remove a like by a user against a blogpost (key)"""
        like_count = 1
        return Likes(blogpost_id=blogpost_id, like_count=like_count,
                     username=username)
# [END Likes data Model]


# [START GQL User datastore & entity types]
class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    # decorators provided by Udacity tutor
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.query().filter(ndb.GenericProperty('name') == name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(name=name,
                    pw_hash=pw_hash,
                    email=email)

        # retained for future ref;
        # see views.py - def users_key(group='default')
        # return User(parent=users_key(),
        #             name=name,
        #             pw_hash=pw_hash,
        #             email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
# [END GQL User datastore & entity types]
