"""
Handler for the MainPage
"""

# [START imports]
from myapp.handlers.basehandler import *
from myapp.models.blogposts import *
from myapp.models.comments import *
from myapp.models.likes import *
from myapp.models.user import *
from myapp.tools.hcookie import check_secure_val
# [END imports]


# [START Main Page]
class MainPage(BaseHandler):
    """Renders the main page with submitted blog posts"""

    def get(self):
        """Renders blogroll with query of latest 10 posts
        & user login/out or signup"""
        posts = ndb.gql(
            "SELECT * from Blogposts ORDER BY created DESC LIMIT 10")

        username = self.request.cookies.get('name')

        if username and username != "":
            self.render("main.html", posts=posts,
                        username=check_secure_val(username))
        else:
            self.render('main.html', posts=posts)
# [END Main Page]
