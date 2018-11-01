#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
from .pages import Page
from .utils.exceptions import SitemapException

logger = logging.getLogger(__name__)

class Sitemap(object):
    """Class responsible to get all posts from file.
    
    The main purpose is to walk the filesystem gathering all files that can be
    a post, generate Post instances and, on those that have 'tags' or 'category'
    headers, create lists of posts for any of them.
    """
    
    def __init__(self, path, extensions=None, encoding='utf-8', keymap_strategy='{filename}'):
        self.path = path
        self.extensions = extensions
        self.encoding = encoding
        self._keymap_strategy = keymap_strategy
    
    @property
    def pages(self):
        try:
            return self._pages
        except AttributeError:
            pass
        pagedict = {}
        def _walker():
            for cur_path, _, filenames in os.walk(self.path):
                for n in filenames:
                    if self.extensions and not n.endswith(self.extensions):
                        continue
                    full_name = os.path.join(cur_path, n)
                    logger.debug('Found page: {0}'.format(full_name))
                    yield full_name
        for filename in _walker():
            try:
                pg = Page(filename, self.encoding, self._keymap_strategy)
                if pg.key not in pagedict:
                    pagedict[pg.key] = pg
                else:
                    raise SitemapException('Key "{0}" exists in the Sitemap.'.format(pg.key))
                logger.debug('Page created: {0}'.format(pg))
            except Exception as e:
                logger.warn('An exception occurred while processing the file: {0}. Ignoring file.'.format(filename, str(e)))
                logger.info(e, exc_info=True)
                continue
        self._pages = pagedict
        return self._pages
    
    @property
    def pagelist(self):
        return self.pages.values()
    
    def filter_by_header(self, header, item=None):
        filtered_pages = (p for p in self.pagelist if header in p.headers)
        for p in filtered_pages:
            if item != None:
                if isinstance(p.headers[header], (list, dict, tuple, set)):
                    if item not in p.headers[header]:
                        continue
                elif item != p.headers[header]:
                    continue
            yield p
    
    def header_values(self, header):
        filtered_pages = (p for p in self.pagelist if header in p.headers)
        s = set()
        for p in filtered_pages:
            if isinstance(p.headers[header], (list, dict, tuple, set)):
                for item in p.headers[header]:
                    if item in s:
                        continue
                    else:
                        s.add(item)
                        yield item
            else:
                if p.headers[header] in s:
                    continue
                else:
                    s.add(p.headers[header])
                    yield p.headers[header]
    
    def __iter__(self):
        return iter(self.pages)
    
    @property
    def keymap_strategy(self):
        return self._keymap_strategy
    
    @keymap_strategy.setter
    def keymap_strategy(self, value):
        self._keymap_strategy = value
        self.reload()
