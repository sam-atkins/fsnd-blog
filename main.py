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
    def render_newpost(self):
        self.render("newpost.html")

    def get(self):
        self.render_newpost()

# [END New Post]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost)
], debug=True)
# [END app]
