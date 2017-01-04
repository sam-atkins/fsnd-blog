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


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
# [END template mgmt & BaseHandler]


# [START Main Page]
class MainPage(BaseHandler):
    def render_main(self):
        self.render("main.html")

    def get(self):
        self.render_main()
# [END Main Page]


# [START New Post]
class NewPost(BaseHandler):
    def render_newpost(self, title="", blogPost="", error=""):
        self.render("newpost.html", title=title,
                    blogPost=blogPost, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        blogPost = self.request.get("blogPost")

        if title and blogPost:
            self.redirect("/thanks")
        else:
            error = "Please submit both a title and a blogpost!"
            self.render_newpost(title, blogPost, error)
# [END New Post]


# [START Thanks page - temp]
class Thanks(BaseHandler):
    def get(self):
        self.render("thanks.html")
# [END Thanks page - temp]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/thanks', Thanks),
], debug=True)
# [END app]
