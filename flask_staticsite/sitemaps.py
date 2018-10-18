#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from . import compatibility
from .page import Page
from .utils.exceptions import SitemapException

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
hdl = logging.StreamHandler()
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdl.setFormatter(fmt)
logger.addHandler(hdl)

class Sitemap(object):
    """Class responsible to get all posts from file.
    
    The main purpose is to walk the filesystem gathering all files that can be
    a post, generate Post instances and, on those that have 'tags' or 'category'
    headers, create lists of posts for any of them.
    """
    
    def __init__(self, path, extensions, encoding, key_mapper):
        self.path = path
        self.extensions = extensions
        self.encoding = encoding
        self._key_mapper = key_mapper
    
    @property
    def key_mapper(self):
        return self._key_mapper
    
    @key_mapper.setter
    def key_mapper(self, value):
        self._key_mapper = value
        self.reload()
    
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
                    yield full_name
        for filename in _walker():
            try:
                pg = Page(filename, encoding=self.encoding, key_mapper=self._key_mapper)
                if pg.key not in pagedict:
                    pagedict[pg.key] = pg
                else:
                    raise SitemapException('Key "{0}" exists in the Sitemap.'.format(pg.key))
            except Exception as e:
                logger.info('An exception occurred while processing the file: {0}. Ignoring file.'.format(filename, str(e)))
                logger.debug(e, exc_info=True)
                continue
        self._pages = pagedict
        return self._pages
    
    def pages_by_header(self, header, item=None):
        l = {kw: p for kw, p in self.pages.items() if header in p.meta}
        if item == None:
            return l
        else:
            for kw, p in l.items():
                if isinstance(p.meta[header], (list, dict, tuple, set)):
                    if item not in p.meta[header]:
                        continue
                elif item != p.meta[header]:
                    continue
                yield kw, p
    
    def header_values(self, header):
        l = {kw: p for kw, p in self.pages.items() if header in p.meta}
        s = set()
        for p in l.values():
            if isinstance(p.meta[header], (list, dict, tuple, set)):
                for item in p.meta[header]:
                    if item in s:
                        continue
                    else:
                        s.add(item)
                        yield item
            else:
                if p.meta[header] in s:
                    continue
                else:
                    s.add(p.meta[header])
                    yield p.meta[header]

    
    def reload(self):
        try:
            del self._pages
        except NameError:
            pass
    
    def __iter__(self):
        return compatibility.itervalues(self.pages)
