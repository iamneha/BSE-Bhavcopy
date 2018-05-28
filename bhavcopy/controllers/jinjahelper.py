#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class JinjaHelper:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_template(self, path):
        try:
            env = Environment(
                loader=FileSystemLoader([
                    '{0}/views'.format(self.base_path),
                    '{0}/views/{1}'.format(self.base_path, path)
                ])
            )
            return env.get_template(path)
        except TemplateNotFound:
            return None
