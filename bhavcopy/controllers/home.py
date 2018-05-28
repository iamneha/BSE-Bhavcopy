import cherrypy
from models.bse_model import BSEModel
from controllers.base import BaseController


class HomeController(BaseController):
    @cherrypy.expose
    def index(self, limit=10):
        return self.render_template(
            'index.html',
            BSEModel.limit(limit)
        )

    @cherrypy.expose
    def search(self, pattern='', limit=10):
        return self.render_template(
            'index.html',
            BSEModel.search(pattern)[:limit]
        )
