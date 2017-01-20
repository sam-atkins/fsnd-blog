"""
Handler for user Register: Inherits from Signup
Completes the registration of a user i.e. put()
of use details to ndb
"""

# [START imports]
from myapp.handlers.signup import SignUp
from myapp.models.user import *
from myapp.tools.hcookie import make_secure_val
# [END imports]


# [START Register]
class Register(SignUp):
    """
    Inherits from the Signup handler.
    Manages user duplication error if username already exists.
    If username is valid, puts new user details to the datastore,
    sets a cookie and redirects to the home page."""

    def done(self):
        """Performs final check on unique username, puts user details to ndb"""

        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            error = 'That user already exists.'
            self.render('signup.html', error_username=error)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            # set cookie
            self.response.headers.add_header(
                'Set-Cookie', 'name=%s; Path=/'
                % str(make_secure_val(self.username)))
            self.redirect('/')
# [END Register]
