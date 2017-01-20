"""
ndb Model: User
Includes methods for:
- user registration, login and finding a user's id
"""

from google.appengine.ext import ndb
from myapp.tools.hpw import make_pw_hash, valid_pw


# [START GQL User datastore & entity types]
class User(ndb.Model):
    """Data Model for Users, with supporting classmethods"""
    name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    # decorators provided by Udacity tutor
    @classmethod
    def by_id(cls, uid):
        """Finds the user's id"""
        return User.get_by_id(uid)

    @classmethod
    def by_name(cls, name):
        """Query to find a username. Used to ensure all usernames are unique"""
        u = User.query().filter(ndb.GenericProperty('name') == name).get()
        return u

    @classmethod
    def register(cls, name, pword, email=None):
        """Used during registration to hash a password"""
        pw_hash = make_pw_hash(name, pword)
        return User(name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pword):
        """Validates a login attempt"""
        u = cls.by_name(name)
        if u and valid_pw(name, pword, u.pw_hash):
            return u
# [END GQL User datastore & entity types]
