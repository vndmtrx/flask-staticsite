#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import current_app, _app_ctx_stack, abort

class StaticSite(object):
    
    default_config = {
        'root': 'posts',
        'extensions': ['html'],
        'encoding': 'utf-8',
        'auto_reload': True
    }
    
    def __init__(self, app=None, name=None):
        self._sitemaps = dict()
        self.name = name
        self.config_prefix = 'STATICSITE' if name is None else '_'.join(('STATICSITE', name.upper()))
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        for kw, val in self.default_config:
            config_kw = '_'.join((self.config_prefix, kw.upper()))
            app.config.setdefault(config_kw, val)
            
        app.before_request(self._auto_reload)
        app.teardown_appcontext(self.teardown)
    
    def config(self, key):
        return self.app.config['_'.join((self.config_prefix, key))]
    
    def create_sitemap(self, path, key_mapper):
        pth = os.path.join(self.config('root'), path)
        ext = self.config('extensions')
        enc = self.config('encoding')
        
        s = Sitemap(pth, ext, enc, key_mapper)
        self._sitemaps['path'] = s
    
    def get_sitemap(self, path):
        return self._sitemaps[path]
    
    def _auto_reload(self):
        for sitemap in self._sitemaps:
            if self.config('auto_reload'):
                sitemap.reload()
    
    def teardown(self, exception):
        pass
