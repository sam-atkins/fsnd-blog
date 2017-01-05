# [START imports]
import os
import webapp2
import jinja2

from google.appengine.ext import db
# [END imports]


# [START template mgmt & BaseHandler]
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


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
# [END template mgmt & BaseHandler]


# [START db Key]
def blog_key(name='default'):
    """Defines the key for the datastore entity i.e. data objects"""
    return db.Key.from_path('blogs', name)
# [END db Key]


# [START GQL datastore & entity types]
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


# [START Thanks page - temp]
class Thanks(BaseHandler):
    def get(self):
        self.render("thanks.html")
# [END Thanks page - temp]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/([0-9]+)', PostPage),
    ('/thanks', Thanks),
], debug=True)
# [END app]
