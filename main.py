"""
Includes all webapp2.WSGIApplication routes
"""

# [START imports]
import webapp2

from myapp.views import *
from myapp.models import *
# [END imports]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/([0-9]+)', PostPage),
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
