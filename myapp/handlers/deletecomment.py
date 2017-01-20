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
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Delete comment]
class DeleteComment(BaseHandler):
    """
    Allows a commentator to delete their comment
    """

    def get(self, comments_id):
        """Renders delete comment page. Restrictions managed via Jinja template:
        only comment author may delete own comments"""

        u = self.request.cookies.get('name')
        self.username = check_secure_val(u)

        # get key for comment
        key = ndb.Key('Comments', int(comments_id))
        comment = key.get()

        self.render("deletecomment.html", comment=comment,
                    username=self.username)

    def post(self, comments_id):
        """Allows comment to be deleted by the comment author"""

        username = self.request.cookies.get('name')
        comment = self.request.get("comment")

        # get key for comment
        key = ndb.Key('Comments', int(comments_id))
        c = key.get()

        # delete
        c.comment = comment
        c.commentator = check_secure_val(username)
        c.key.delete()

        self.redirect('/')
# [END Delete Comment]
