# [START imports]
import os
import webapp2
import jinja2
import re
import hashlib
import hmac
import random
import string

import secret_stuff

from google.appengine.ext import db
# [END imports]


# [START template mgmt & BaseHandler & cookies]
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# def render_str(self, template, **params):
#     """takes as inputs a template and a dictionary of params"""
#     t = jinja_env.get_template(template)
#     return t.render(params)


def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret_stuff.SECRET, val).hexdigest)


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


# check return cookie after logout
# COOKIE_RE = re.compile(r'.+=;\s*Path=/')
# def valid_cookie(cookie):
#     return cookie and COOKIE_RE.match(cookie)

# Convenience functions
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

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.reponse.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """Reads and checks the cookie is valid"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and Users.by_id(int(uid))


def render_post(response, blogpost):
    response.out.write('<b>' + blogpost.subject + '</b><br>')
    response.out.write(blogpost.content)
# [END template mgmt & BaseHandler & cookies]


# [START db Key]
def blog_key(name='default'):
    """Defines the key for the datastore entity i.e. data objects"""
    return db.Key.from_path('blogs', name)
# [END db Key]


# [START GQL Blogposts datastore & entity types]
class Blogposts(db.Model):
    """
    this class enables adding to the App Engine database,
    and specifies the entity data types
    """
    title = db.StringProperty(required=True)
    blogPost = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    # required=True is a constraint enforces posts to db must have a title
    # auto_add_now adds an entry automatically with every submission
# [END GQL datastore & entity types]


# [START GQL User datastore & entity types]
# makes a salt from 5 random letters
# py2 = string.letters / # py3 = string.ascii_letters
def make_salt(length=5):
    return "".join(random.choice(string.letters) for x in range(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()

    h = name + pw + salt
    return '%s|%s' % (hashlib.sha256(h.encode('utf-8')).hexdigest(), salt)


def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)

# solution code; enables user-groups


def users_key(group='default'):
    return db.Key.from_path('users', group)


class Users(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()      # no required statement as user optional

    # decorators
    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return cls(parent=users_key(),
                   name=name,
                   pw_hash=pw_hash,
                   email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
# [END GQL User datastore & entity types]


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

# Regex for form error handling
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_PW = re.compile(r"^.{3,20}$")
USER_EM = re.compile(r"^[\S]+@[\S]+.[\S]+$")


# helper functions for Signup Handler
def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and USER_RE.match(password)


def valid_email(email):
    return not email or USER_EM.match(email)


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


class Register(SignUp):
    def done(self):
        # make sure the user doesn't already exist
        u = Users.by_name(self.username)
        if u:
            error = 'That user already exists.'
            self.render('signup.html', error_username=error)
        else:
            u = Users.register(self.username, self.password, self.email)
            u.put()

            # set cookie or login
            self.login(u)
            self.redirect('/welcome')


# [START Welcome]
class Welcome(BaseHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
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

        u = Users.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
# [END name]


# [START Logout]
class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/welcome')
        self.redirect('signup')
# [END name]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/([0-9]+)', PostPage),
    # ('/signup-form', SignUp),
    ('/signup', Register),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/logout', Logout)
], debug=True)
# [END app]
