"""
Handler for user Signup
"""

# [START imports]
from myapp.handlers.basehandler import BaseHandler
from myapp.tools.validform import valid_username, valid_password, valid_email
# [END imports]


# [START Sign-up]
class SignUp(BaseHandler):
    """Manages user signup, including error handling if form is not
    completed correctly."""

    def get(self):
        """Renders signup form"""
        self.render("signup.html")

    def post(self):
        """Manages correct entry of signup form, with error handling"""
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        """Once complete passed to the Register Handler"""
        raise NotImplementedError
# [END Sign-up]
