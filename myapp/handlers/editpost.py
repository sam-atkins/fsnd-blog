"""
Handler for EditPost
Manages the editing of blog posts
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Edit post page]
class EditPost(BaseHandler):
    """
    Renders the permalink/edit page with the blogpost content
    for the user to edit. If a bad url, sends to the 404 page.
    Only author of the post may edit, control managed via Jinja template
    """

    def get(self, post_id):
        """Allows the author to edit the post page"""
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("editpost.html", post=post,
                    username=check_secure_val(username))

    def post(self, post_id):
        """
        If edit is valid, adds edited post to db and redirects back to
        permalink page.
        If invalid, displays error message, and renders same form.
        """

        title = self.request.get("title")
        blogPost = self.request.get("blogPost")

        if title and blogPost:

            blogPost_key = ndb.Key(
                'Blogposts', int(post_id), parent=blog_key())
            bp = blogPost_key.get()
            bp.title = title
            bp.blogPost = blogPost
            bp.put()

            self.redirect('/%s' % str(bp.key.integer_id()))
        else:
            username = self.request.cookies.get('name')
            error = "Please submit both a title and a blogpost!"
            self.render("newpost.html", username=check_secure_val(username),
                        title=title, blogPost=blogPost, error=error)
# [END Edit post page]
