"""
BaseHandler used by all other handlers
"""

# [START imports]
import os
import webapp2
import jinja2

from myapp.tools.hcookie import make_secure_val, check_secure_val
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
# [END imports]


# global varirables for use of Jinja templates
template_dir = os.path.join(os.path.dirname(__file__) + '/../../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# [START template mgmt & BaseHandler & cookies]
class BaseHandler(webapp2.RequestHandler):
    """
    Base Handler used by all Page Handlers.
    Also, includes functions to set, read and check cookies.
    """

    def write(self, *args, **kwargs):
        """shortcut to writing 'response.out.write' """
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        """takes as inputs a template and params"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        """calls write and render_str to render a template"""
        self.write(self.render_str(template, **kwargs))

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
    Solution code from Udacity tutor. Renders title and content of blogposts.
    """
    response.out.write('<b>' + Blogposts.title + '</b><br>')
    response.out.write(Blogposts.blogPost)
# [END template mgmt & BaseHandler & cookies]


# [START db keys for blogs and user groups]
def blog_key(name='default'):
    """Defines the key for the datastore entity i.e. data objects"""

    return ndb.Key('blogs', name)
# [END db keys for blogs and user groups]
