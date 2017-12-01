#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

db = {
    'alice@example.com': ['groceries', 'laundry'],
    'bob@example.com': ['cut the grass']
}


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            if user.nickname() in db:
                todos = db[user.nickname()]
            else:
                todos = []
            logout_url = users.create_logout_url('/')
            return self.render_template("user.html", {'user': user.nickname(), 'logout_url': logout_url, 'todos': todos})
        else:
            login_url = users.create_login_url('/')

            return self.render_template("guest.html", {'user': user, 'login_url': login_url})


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
