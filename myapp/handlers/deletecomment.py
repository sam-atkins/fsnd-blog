"""
Handler for DeleteComment
Allows users who own a comment to delete that comment
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


# [START Delete comment]
class DeleteComment(BaseHandler):
    """
    Allows a commentator to delete their comment
    """

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comments_id, c):
        """Renders delete comment page. Restrictions managed via Jinja template:
        only comment author may delete own comments"""

        u = self.request.cookies.get('name')
        self.username = check_secure_val(u)
        self.render("deletecomment.html", comment=c,
                    username=self.username)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comments_id, c):
        """Allows comment to be deleted by the comment author"""

        username = self.request.cookies.get('name')
        comment = self.request.get("comment")

        # delete
        c.comment = comment
        c.commentator = check_secure_val(username)
        c.key.delete()

        self.redirect('/')
# [END Delete Comment]
