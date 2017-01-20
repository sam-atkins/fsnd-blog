"""
Handler for LikePage
Manages the like / unlike of pages
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.handlers.postpage import PostPage
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Like blogposts Handler]
class LikePage(PostPage):
    """
    Inherits from the post page
    Enables like and unlike of blogposts
    """

    def post(self, post_id):
        """Enables like and unlike blogposts"""

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        comments = Comments.query(Comments.blogpost_id == int(
            post_id)).order(Comments.comment_date)

        # like counter query for permalink page
        likes = Likes.query().filter(Likes.blogpost_id == int(post_id)).fetch(
            projection=[Likes.like_count])

        post_id = int(post_id)
        self.username = self.request.cookies.get('name')

        # 1 get blogpost entity key
        self.blogPost_key = ndb.Key(
            'Blogposts', int(post_id), parent=blog_key())
        self.bp = self.blogPost_key.get()

        # 2 if author, provide error message
        if self.bp.author == check_secure_val(self.username):
            error_likes = "Sorry, you can't like your own blogpost!"
            self.render("permalink.html", post=post, key=key,
                        comments=comments, likes=likes,
                        username=check_secure_val(self.username),
                        error_likes=error_likes)

        else:

            check_like = Likes._check_like(post_id, self.username)

            # 3 if user has already liked the post, delete the like from ndb
            if check_like:

                # get the id
                like_id = Likes._find_like_key(post_id, self.username)

                # get the key
                like = like_id._key.get()

                # delete
                like.key.delete()

                self.render("permalink.html", post=post, key=key,
                            comments=comments, likes=likes,
                            username=check_secure_val(self.username))

            # 4 if user has not yet liked the post, add a like to ndb
            else:
                add_like = Likes._add_like(post_id, self.username)
                add_like.put()
                self.render("permalink.html", post=post, key=key,
                            comments=comments, likes=likes,
                            username=check_secure_val(self.username))
# [END Like blogposts Handler]
