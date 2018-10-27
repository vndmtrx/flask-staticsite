#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from .sitemaps import Sitemap
from flask import current_app, _app_ctx_stack, abort

class StaticSite(object):
    
    default_config = {
        'root': 'posts',
        'extensions': [],
        'encoding': 'utf-8',
        'keymap_strategy': '{filename}',
        'auto_reload': True
    }
    
    def __init__(self, app=None, name=None):
        self.name = name
        self.config_prefix = 'STATICSITE' if name is None else '_'.join(('STATICSITE', name.upper()))
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        for kw, val in self.default_config.items():
            config_kw = '_'.join((self.config_prefix, kw.upper()))
            app.config.setdefault(config_kw, val)
        
        app.before_request(self._auto_reload)
        app.teardown_appcontext(self.teardown)
        
        if 'staticsite' not in app.extensions:
            app.extensions['staticsite'] = {}
        app.extensions['staticsite'][self.name] = self
        
        self.app = app
        
        pth = self.config('root')
        ext = self.config('extensions')
        enc = self.config('encoding')
        keymap = self.config('keymap_strategy')
        self._sitemap = Sitemap(pth, ext, enc, keymap)
    
    def config(self, key):
        return self.app.config['_'.join((self.config_prefix, key.upper()))]
    
    def _auto_reload(self):
        if self.config('auto_reload'):
            sitemap.reload()
    
    def teardown(self, exception):
        pass

    @property
    def sitemap(self):
        return self._sitemap
