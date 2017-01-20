"""
ndb Model: Comments
"""

from google.appengine.ext import ndb


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
# [END Comments Model]
