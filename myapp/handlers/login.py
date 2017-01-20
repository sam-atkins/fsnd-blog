"""
Handler for Login
"""

# [START imports]
from myapp.handlers.basehandler import BaseHandler
from myapp.models.user import *
from myapp.tools.hcookie import make_secure_val
# [END imports]


# [START Login]
class Login(BaseHandler):
    """
    Manages user login, using the User Model (datastore) and the decorator,
    i.e. the @class method login. If the user's username and password are
    valid, a cookie is set and the user is redirected to the home page.
    If invalid, the login form is rendered with an error message.
    """

    def get(self):
        """Renders login form"""
        self.render('login-form.html')

    def post(self):
        """Validates user login details, manages errors, and
        redirects to home if successful"""

        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            # set cookie
            self.response.headers.add_header(
                'Set-Cookie', 'name=%s; Path=/'
                % str(make_secure_val(username)))
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
# [END name]
