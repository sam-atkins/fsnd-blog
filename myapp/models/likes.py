"""
ndb Model: Likes
Includes methods for:
- finding like id, adding a like,
- checking if user already liked a post
"""

from google.appengine.ext import ndb


# [START Likes data Model]
class Likes(ndb.Model):
    """Model for Likes for a blogpost"""
    blogpost_id = ndb.IntegerProperty(required=True)
    like_count = ndb.IntegerProperty(required=True)
    username = ndb.StringProperty(required=True)

    @classmethod
    def _check_like(cls, post_id, username):
        """
        Checks if a blogpost (via the post_id key) already
        has a like by the user"""

        query = Likes.query().filter(Likes.blogpost_id == post_id).filter(
            Likes.username == username).get()
        if query:
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
# [END Likes data Model]
