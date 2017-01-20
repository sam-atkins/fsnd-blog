"""
Handler for NewPost
Manages the create and posting of new blog posts
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.user import *
from myapp.tools.decorators import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START New Post]
class NewPost(BaseHandler):
    """Renders the new post page with post entry form"""

    @user_logged_in
    def get(self):
        """Renders form to submit new blogpost"""
        username = self.request.cookies.get('name')
        self.render("newpost.html", title="",
                    blogPost="", error="",
                    username=check_secure_val(username))

    @user_logged_in
    def post(self):
        """
        If submission is valid, adds to db and redirects to permalink page.
        If invalid, displays error message, and renders same form."""

        title = self.request.get("title")
        blogPost = self.request.get("blogPost")
        author = self.request.cookies.get('name')

        if title and blogPost:

            bp = Blogposts(parent=blog_key(), title=title,
                           blogPost=blogPost, author=check_secure_val(author))

            bp.put()

            self.redirect('/%s' % str(bp.key.integer_id()))
        else:
            error = "Please submit both a title and a blogpost!"
            self.render("newpost.html", title=title,
                        blogPost=blogPost, error=error)
# [END New Post]
