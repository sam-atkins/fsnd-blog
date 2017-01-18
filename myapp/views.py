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
        """takes as inputs a template and params"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """calls write and render_str to render a template"""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """
        Sets cookie. No expire time is set, meaning user session
        expires when browser closed
        """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """Checks cookie val and if valid, returns the cookie value"""
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)


def render_post(response, Blogposts):
    """
    Solution code from Udacity tutor.
    """
    response.out.write('<b>' + Blogposts.title + '</b><br>')
    response.out.write(Blogposts.blogPost)
# [END template mgmt & BaseHandler & cookies]


# [START db keys for blogs and user groups]
def blog_key(name='default'):
    """Defines the key for the datastore entity i.e. data objects"""

    return ndb.Key('blogs', name)
# [END db keys for blogs and user groups]


# Enables user-groups
# def users_key(group='default'):
    """
    Solution code from Udacity tutor, retained for future
    learning/study. It enables user-groups by assigning each user to a group
    within the datastore
    """

    # return ndb.Key('users', group)
# [END db db keys for blogs and user groups]


# [START Main Page]
class MainPage(BaseHandler):
    """Renders the main page with submitted blog posts"""

    def get(self):
        posts = ndb.gql(
            "SELECT * from Blogposts ORDER BY created DESC LIMIT 10")

        username = self.request.cookies.get('name')

        if username and username != "":
            self.render("main.html", posts=posts,
                        username=check_secure_val(username))
        else:
            self.render('main.html', posts=posts)
# [END Main Page]


# [START New Post]
class NewPost(BaseHandler):
    """Renders the new post page with post entry form"""

    def get(self):
        username = self.request.cookies.get('name')
        self.render("newpost.html", title="",
                    blogPost="", error="",
                    username=check_secure_val(username))

    def post(self):
        """
        If submission is valid, adds to db and redirects to permalink page.
        If invalid, displays error message, and renders same form."""

        title = self.request.get("title")
        blogPost = self.request.get("blogPost")
        author = self.request.cookies.get('name')

        if title and blogPost:

            bp = Blogposts(parent=blog_key(), title=title,
                           blogPost=blogPost, author=check_secure_val(author))

            bp.put()

            self.redirect('/%s' % str(bp.key.integer_id()))
        else:
            error = "Please submit both a title and a blogpost!"
            self.render("newpost.html", username=check_secure_val(
                username), title=title, blogPost=blogPost, error=error)
# [END New Post]


# [START Permalink post page]
class PostPage(BaseHandler):
    """Renders the permalink page or if a bad url, sends to the 404 page."""

    def get(self, post_id):
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        comments = Comments.query(Comments.blogpost_key == int(
            post_id)).order(Comments.comment_date)

        # like counter query for permalink page
        likes = Likes.query().filter(Likes.blogpost_key == int(post_id)).fetch(
            projection=[Likes.like_count])

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, key=key, comments=comments,
                    likes=likes, username=check_secure_val(username))

    def post(self, post_id):
        """
        like and unlike blogposts
        """

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        comments = Comments.query(Comments.blogpost_key == int(
            post_id)).order(Comments.comment_date)

        # like counter query for permalink page
        likes = Likes.query().filter(Likes.blogpost_key == int(post_id)).fetch(
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
# [END Permalink post page]


# [START Edit post page]
class EditPost(BaseHandler):
    """
    Renders the permalink/edit page with the blogpost content
    for the user to edit.
    If a bad url, sends to the 404 page.
    """

    def get(self, post_id):
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("editpost.html", post=post,
                    username=check_secure_val(username))

    def post(self, post_id):
        """
        If edit is valid, adds edited post to db and redirects back to
        permalink page.
        If invalid, displays error message, and renders same form.
        """

        title = self.request.get("title")
        blogPost = self.request.get("blogPost")

        if title and blogPost:

            blogPost_key = ndb.Key(
                'Blogposts', int(post_id), parent=blog_key())
            bp = blogPost_key.get()
            bp.title = title
            bp.blogPost = blogPost
            bp.put()

            self.redirect('/%s' % str(bp.key.integer_id()))
        else:
            username = self.request.cookies.get('name')
            error = "Please submit both a title and a blogpost!"
            self.render("newpost.html", username=check_secure_val(username),
                        title=title, blogPost=blogPost, error=error)
# [END Edit post page]


# [START Delete post page]
class DeletePost(BaseHandler):
    """
    Renders the permalink page with the blogpost content and
    if the user clicks submit, the blog post is deleted.
    If a bad url, sends to the 404 page.
    """

    def get(self, post_id):
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("deletepost.html", post=post,
                    username=check_secure_val(username))

    def post(self, post_id):
        """
        If user hits delete button, post is deleted and returned to home page.
        """

        title = self.request.get("title")
        blogPost = self.request.get("blogPost")
        author = self.request.cookies.get('name')

        blogPost_key = ndb.Key(
            'Blogposts', int(post_id), parent=blog_key())
        bp = blogPost_key.get()
        bp.title = title
        bp.blogPost = blogPost
        bp.author = check_secure_val(author)
        bp.key.delete()
        self.redirect('/')
# [END Delete post page]


# [START Comment]
class Comment(BaseHandler):
    """Adds comments to a permalink blogpost"""

    def get(self, post_id):
        username = self.request.cookies.get('name')

        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("comment.html", post=post,
                    username=check_secure_val(username))

    def post(self, post_id):
        """
        If comment submission is valid, adds to db and redirects to
        permalink page.
        If invalid, displays error message, and renders same form.
        """

        # info for redirect to permalink page
        # refactor using Friendly URL routing in webapp2
        key = ndb.Key('Blogposts', int(post_id), parent=blog_key())
        blogPost_key = ndb.Key(
            'Blogposts', int(post_id), parent=blog_key())
        bp = blogPost_key.get()
        post = key.get()

        username = self.request.cookies.get('name')
        comment = self.request.get("comment")
        c = self.request.cookies.get('name')
        commentator = check_secure_val(c)

        if comment != "":

            # 1 - blogpost key is the post_id of blogpost
            blogpost_key = int(post_id)

            # 2 - create Comment instance and assign comment data types
            c = Comments(blogpost_key=blogpost_key, comment=comment,
                         commentator=commentator)

            # 3 - put comment types to ndb
            c.put()

            if not post:
                self.error(404)
                return

            self.redirect('/%s' % str(bp.key.integer_id()))

        else:
            error = "Please submit a comment!"
            self.render("comment.html", post=post, error=error,
                        username=check_secure_val(username))
# [END Comment]


# [START Sign-up]
class SignUp(BaseHandler):
    """Manages user signup, including error handling if form is not
    completed correctly."""

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
    """
    Inherits from the Signup handler.
    Manages user duplication error if username already exists.
    If username is valid, puts new user details to the datastore,
    sets a cookie and redirects to the welcome page."""

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
            # test:
            # self.redirect('/welcome')
            self.redirect('/')
# [END Register]


# [START Welcome]
class Welcome(BaseHandler):
    """
    This is the redirect from a successful signup or login
    Checks if there is a username and that the username is not blank ie " "
    If OK, renders welcome.html, and confirms the secure cookie
    Otherwise, redirects to signup.
    """

    def get(self):
        username = self.request.cookies.get('name')
        if username and username != "":
            self.render('welcome.html', username=check_secure_val(username))
        else:
            self.redirect('/signup')
# [END Welcome]


# [START Login]
class Login(BaseHandler):
    """
    Manages user login, using the User Model (datastore) and the decorator,
    i.e. the @class method login. If the user's username and password are
    valid, a cookie is set and the user is redirected to welcome.
    If invalid, the login form is rendered with an error message.
    """

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
            # test:
            # self.redirect('/welcome')
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
# [END name]


# [START Logout]
class Logout(BaseHandler):
    """
    Manages user logout, by setting the cookie value to zero
    'name=;' - this has the effect of deleting the cookie.
    User is redirected to the homepage
    """

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect('/')
# [END name]
