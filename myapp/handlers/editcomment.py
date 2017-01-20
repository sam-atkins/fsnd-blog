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
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Edit comment]
class EditComment(BaseHandler):
    """
    Allows a commentator to edit their comment
    """

    def get(self, comments_id):
        """Renders form to edit a comment. Only author of comment
        may edit, control managed via Jinja template"""

        u = self.request.cookies.get('name')
        self.username = check_secure_val(u)

        # get key for comment
        key = ndb.Key('Comments', int(comments_id))
        comment = key.get()

        self.render("editcomment.html", comment=comment,
                    username=self.username)

    def post(self, comments_id):
        """Allows author to edit a comment and post to ndb"""

        username = self.request.cookies.get('name')
        comment = self.request.get("comment")

        # get key for comment
        key = ndb.Key('Comments', int(comments_id))
        c = key.get()

        if comment != "":
            c.comment = comment
            c.put()
            self.redirect('/')

        else:
            error = "Please submit a comment!"
            self.render("comment.html", error=error,
                        username=check_secure_val(username))
# [END Edit Comment]
