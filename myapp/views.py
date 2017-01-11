# [START imports]
import os
import webapp2
import jinja2

from hcookie import *
from hpw import *
from validform import *
from models import *
# [END imports]


# [START template mgmt & BaseHandler & cookies]
template_dir = os.path.join(os.path.dirname(__file__) + '/../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        """shortcut to writing 'response.out.write' """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """takes as inputs a template and a dictionary of params"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """calls write and render_str to render a template"""
        self.write(self.render_str(template, **kw))

    # no expire time incl; will expire when browser closed
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)


def render_post(response, blogpost):
    response.out.write('<b>' + blogpost.subject + '</b><br>')
    response.out.write(blogpost.content)
# [END template mgmt & BaseHandler & cookies]


# [START db keys for blogs and user groups]
def blog_key(name='default'):
    """Defines the key for the datastore entity i.e. data objects"""
    return db.Key.from_path('blogs', name)


# solution code; enables user-groups
def users_key(group='default'):
    return db.Key.from_path('users', group)
# [END db db keys for blogs and user groups]


# [START Main Page]
class MainPage(BaseHandler):
    """renders the main page with submitted blog posts"""

    def get(self):
        posts = db.GqlQuery(
            "SELECT * from Blogposts ORDER BY created DESC LIMIT 10")
        self.render("main.html", posts=posts)
# [END Main Page]


# [START New Post]
class NewPost(BaseHandler):
    def render_newpost(self, title="", blogPost="", error=""):
        self.render("newpost.html", title=title,
                    blogPost=blogPost, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        """
        if submission is valid, adds to db and redirects
        to thanks page
        if invalid, displays error message, and renders same form
        """
        title = self.request.get("title")
        blogPost = self.request.get("blogPost")

        if title and blogPost:
            bp = Blogposts(parent=blog_key(), title=title, blogPost=blogPost)
            bp.put()

            # self.redirect("/thanks")
            self.redirect('/%s' % str(bp.key().id()))
        else:
            error = "Please submit both a title and a blogpost!"
            self.render_newpost(title, blogPost, error)
# [END New Post]


# [START Permalink post page]
class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Blogposts', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)
# [END Permalink post page]


# [START Sign-up]
class SignUp(BaseHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
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
        raise NotImplementedError
# [END Sign-up]


# [START Register]
class Register(SignUp):
    def done(self):
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
            self.redirect('/welcome')
# [END Register]


# [START Welcome]
class Welcome(BaseHandler):
    def get(self):
        username = self.request.cookies.get('name')
        if username and username != "":
            self.render('welcome.html', username=check_secure_val(username))
        else:
            self.redirect('/signup')
# [END Welcome]


# [START Login]
class Login(BaseHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            # set cookie
            self.response.headers.add_header(
                'Set-Cookie', 'name=%s; Path=/'
                % str(make_secure_val(username)))
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
# [END name]


# [START Logout]
class Logout(BaseHandler):
    def get(self):
        # set cookie to name = zero value; i.e. delete it
        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect('/')
# [END name]
