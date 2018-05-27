#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
from controllers.jinjahelper import JinjaHelper
import logging


logger = logging.getLogger(__name__)


class BaseController:
    def render_template(self, path, data=None):
        data = data or {}
        try:
            jh = JinjaHelper(cherrypy.site['base_path'])
            template = jh.get_template(path)
            if not template:
                logger.error('Error rendering template: ' + path, None, True)
            return template.render(data=data)
        except Exception as ex:
            logger.error('Error rendering template', ex, True)
