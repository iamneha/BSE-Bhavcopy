#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
base_path = os.path.abspath(os.path.dirname(__file__))
config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8000,
        'server.thread_pool': 4,
        'tools.trailing_slash.on': False,
        'tools.staticdir.root': base_path
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static'
    }
}
