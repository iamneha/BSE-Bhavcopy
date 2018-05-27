import cherrypy
import config
import logging
from controllers.home import HomeController

logger = logging.getLogger(__name__)


def start_server():
    cherrypy.site = {
        'base_path': config.base_path
    }
    cherrypy.config.update(config.config)
    cherrypy.tree.mount(HomeController(), '/', config.config)
    cherrypy.engine.start()
    return cherrypy.tree


try:
    logger.info("Downloading data.....")
    logger.info("FINISHED!")
    application = start_server()
except Exception as ex:
    logger.error('Error during run', ex)
