#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# flask_staticsite.staticsite

StaticSite extension.
"""

import operator
import os

from inspect import getargspec
from itertools import takewhile

from flask import abort
from werkzeug.utils import cached_property, import_string

from . import compat
from .page import Page
from .utils import force_unicode


class StaticSite(object):

    default_config = (
        ('search_path', 'pages'),
        ('extension', '.txt'),
        ('encoding', 'utf-8'),
        ('auto_reload', 'if debug'),
    )

    def __init__(self, app=None, name=None):
        self.name = name
        self.config_prefix = 'STATICSITE' if name is None else '_'.join(('STATICSITE', name.upper()))
        
        self._file_cache = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        for key, value in self.default_config:
            config_key = '_'.join((self.config_prefix, key.upper()))
            app.config.setdefault(config_key, value)
        
        if 'staticsite' not in app.extensions:
            app.extensions['staticsite'] = {}
        app.extensions['staticsite'][self.name] = self
        self.app = app
    
    def config(self, key):
        return self.app.config['_'.join((self.config_prefix, key.upper()))]
