"""
Handler for Logout
"""

# [START imports]
from myapp.handlers.basehandler import BaseHandler
# [END imports]


# [START Logout]
class Logout(BaseHandler):
    """
    Manages user logout, by setting the cookie value to zero
    'name=;' - this has the effect of deleting the cookie.
    User is redirected to the homepage
    """

    def get(self):
        """User logout, clear cookie, redirect to home as visitor"""

        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect('/')
# [END name]
