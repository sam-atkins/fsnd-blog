"""
Handler for DeletePost
Manages the deleting of blog posts
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.user import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Delete post page]
class DeletePost(BaseHandler):
    """
    Renders the permalink page with the blogpost content and
    if the user clicks submit, the blog post is deleted.
    If a bad url, sends to the 404 page.
    Restrictions/control managed via Jinja template:
    only author may delete their own post.
    """

    def get(self, post_id):
        """Renders the post and presents option for author
        to delete their blogpost"""
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("deletepost.html", post=post,
                    username=check_secure_val(username))

    def post(self, post_id):
        """Allows the author to delete their blogpost"""
        title = self.request.get("title")
        blogPost = self.request.get("blogPost")
        author = self.request.cookies.get('name')

        blogPost_key = ndb.Key(
            'Blogposts', int(post_id), parent=blog_key())
        bp = blogPost_key.get()
        bp.title = title
        bp.blogPost = blogPost
        bp.author = check_secure_val(author)
        bp.key.delete()
        self.redirect('/')
# [END Delete post page]
