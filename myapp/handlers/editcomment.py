"""
Handler for EditComment
Allows user who owns the comment
to edit a comment to a blogpost
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


# [START Edit comment]
class EditComment(BaseHandler):
    """
    Allows a commentator to edit their comment
    """

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comments_id, c):
        """Renders form to edit a comment."""

        u = self.request.cookies.get('name')
        self.username = check_secure_val(u)
        self.render("editcomment.html", comment=c,
                    username=self.username)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comments_id, c):
        """Allows author to edit a comment and post to ndb"""

        username = self.request.cookies.get('name')
        comment = self.request.get("comment")

        if comment != "":
            c.comment = comment
            c.put()
            self.redirect('/')

        else:
            error = "Please submit a comment!"
            self.render("comment.html", error=error,
                        username=check_secure_val(username))
# [END Edit Comment]
