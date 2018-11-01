#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
from .sitemaps import Sitemap
from flask import abort

logger = logging.getLogger(__name__)

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
    
    def config(self, key):
        return self.app.config['_'.join((self.config_prefix, key.upper()))]
    
    def reload(self):
        try:
            del self._sitemap
        except (NameError, AttributeError):
            pass
    
    def _auto_reload(self):
        if self.config('auto_reload'):
            logger.info('Autoreloading...')
            self.reload()
    
    def teardown(self, exception):
        pass

    @property
    def sitemap(self):
        if not hasattr(self, '_sitemap'):
            logger.info('Sitemap not found. Creating...')
            pth = self.path
            ext = self.extensions
            enc = self.encoding
            keymap = self.keymap_strategy
            self._sitemap = Sitemap(pth, ext, enc, keymap)
        return self._sitemap
    
    @property
    def path(self):
        try:
            return self._path
        except (NameError, AttributeError):
            return self.config('root')
    
    @path.setter
    def path(self, value):
        self._path = value
        self.reload()

    @property
    def extensions(self):
        try:
            return self._extensions
        except (NameError, AttributeError):
            return self.config('extensions')
    
    @extensions.setter
    def extensions(self, value):
        self._extensions = value
        self.reload()

    @property
    def encoding(self):
        try:
            return self._encoding
        except (NameError, AttributeError):
            return self.config('encoding')
    
    @encoding.setter
    def encoding(self, value):
        self._encoding = value
        self.reload()

    @property
    def keymap_strategy(self):
        try:
            return self._keymap_strategy
        except (NameError, AttributeError):
            return self.config('keymap_strategy')
    
    @keymap_strategy.setter
    def keymap_strategy(self, value):
        self._keymap_strategy = value
        self.reload()
