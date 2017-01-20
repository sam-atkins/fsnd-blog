"""
Handler for the Comment
Allows users to add a comment to a blogpost
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
from myapp.tools.decorators import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Comment]
class Comment(BaseHandler):
    """Adds comments to a permalink blogpost"""

    @user_logged_in
    def get(self, post_id):
        """Form to add a comment"""
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("comment.html", post=post,
                    username=check_secure_val(username))

    @user_logged_in
    def post(self, post_id):
        """Allows posting of comment on a blogpost"""

        # info for redirect to permalink page
        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        blogPost_key = ndb.Key(
            'Blogposts', int(post_id), parent=blog_key())
        bp = blogPost_key.get()
        post = key.get()

        username = self.request.cookies.get('name')
        comment = self.request.get("comment")
        c = self.request.cookies.get('name')
        commentator = check_secure_val(c)

        if comment != "":

            # 1 - blogpost key is the post_id of blogpost
            blogpost_id = int(post_id)

            # 2 - create Comment instance and assign comment data types
            c = Comments(blogpost_id=blogpost_id, comment=comment,
                         commentator=commentator)

            # 3 - put comment types to ndb
            c.put()

            if not post:
                self.error(404)
                return

            self.redirect('/%s' % str(bp.key.integer_id()))

        else:
            error = "Please submit a comment!"
            self.render("comment.html", post=post, error=error,
                        username=check_secure_val(username))
# [END Comment]
