"""
Handler for PostPage
Manages the create and posting of new blog posts
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Permalink post page]
class PostPage(BaseHandler):
    """Renders the permalink page or if a bad url, sends to the 404 page."""

    def get(self, post_id):
        """Renders permalink page, with query for like count"""
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        comments = Comments.query(Comments.blogpost_id == int(
            post_id)).order(Comments.comment_date)

        # like counter query for permalink page
        likes = Likes.query().filter(Likes.blogpost_id == int(post_id)).fetch(
            projection=[Likes.like_count])

        if not post:
            self.error(404)
        else:
            self.render("permalink.html", post=post, key=key,
                        comments=comments,
                        likes=likes, username=check_secure_val(username))
            # self.done()

        def done(self, *a, **kw):
            """Passed to the LikePost Handler"""
            raise NotImplementedError

# [END Permalink post page]
