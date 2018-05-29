import cherrypy
import config
import logging
import threading
from controllers.home import HomeController
from models.bse_model import BSEModel
from utils.data_fetcher import store_data

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
    threading.Thread(target=store_data, args=(BSEModel, )).start()
    application = start_server()
except Exception as ex:
    logger.error('Error during run', ex)
