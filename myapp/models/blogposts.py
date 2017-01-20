"""
ndb Model: Blogposts
"""

from google.appengine.ext import ndb


# [START GQL Blogposts datastore & entity types]
class Blogposts(ndb.Model):
    """
    Adds blogposts (title, blogPost content, author, created and last
    modified) entity data types to the App Engine database.
    The model class specifies the entity data types."""

    title = ndb.StringProperty(required=True)
    blogPost = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    author = ndb.StringProperty(required=True)
# [END GQL datastore & entity types]
