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
    ('/edit/([0-9]+)', EditPost),
    ('/signup', Register),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/logout', Logout)
], debug=True)
# [END app]
