import cherrypy
from controllers.base import BaseController

class HomeController(BaseController):
    @cherrypy.expose
    def index(self, limit=10):
        return self.render_template('layout.html')

