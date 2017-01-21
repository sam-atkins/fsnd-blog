"""
Handler for DeletePost
Manages the deleting of blog posts
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.user import *
from myapp.tools.decorators import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Delete post page]
class DeletePost(BaseHandler):
    """
    Renders the permalink page with the blogpost content and
    if the user clicks submit, the blog post is deleted.
    If a bad url, sends to the 404 page.
    """

    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id, post):
        """Renders the post and presents option for author
        to delete their blogpost"""

        username = self.request.cookies.get('name')
        if not post:
            self.error(404)
            return
        self.render("deletepost.html", post=post,
                    username=check_secure_val(username))

    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self, post_id, post):
        """Allows the author to delete their blogpost"""

        title = self.request.get("title")
        blogPost = self.request.get("blogPost")
        author = self.request.cookies.get('name')

        post.title = title
        post.blogPost = blogPost
        post.author = check_secure_val(author)
        post.key.delete()
        self.redirect('/')
# [END Delete post page]
