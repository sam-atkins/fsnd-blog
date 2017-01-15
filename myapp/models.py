from google.appengine.ext import ndb

from hpw import *


# [START Author]
class Author(ndb.Model):
    """ sub model for representing an author"""

    author = ndb.StringProperty(required=True)
# [END Author]


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
    author = ndb.StructuredProperty(Author)
# [END GQL datastore & entity types]


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
