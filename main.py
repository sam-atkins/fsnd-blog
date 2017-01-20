"""
Includes all webapp2.WSGIApplication routes
"""

# [START imports]
import webapp2
from myapp.handlers.mainpage import MainPage
from myapp.handlers.newpost import NewPost
from myapp.handlers.likepage import LikePage
from myapp.handlers.editpost import EditPost
from myapp.handlers.deletepost import DeletePost
from myapp.handlers.comment import Comment
from myapp.handlers.editcomment import EditComment
from myapp.handlers.deletecomment import DeleteComment
from myapp.handlers.register import Register
from myapp.handlers.login import Login
from myapp.handlers.logout import Logout
# [END imports]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/([0-9]+)', LikePage),
    ('/edit/post/([0-9]+)', EditPost),
    ('/delete/post/([0-9]+)', DeletePost),
    ('/comment/([0-9]+)', Comment),
    ('/edit/comment/([0-9]+)', EditComment),
    ('/delete/comment/([0-9]+)', DeleteComment),
    ('/signup', Register),
    ('/login', Login),
    ('/logout', Logout)
], debug=True)
# [END app]
