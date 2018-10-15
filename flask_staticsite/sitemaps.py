#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from . import compatibility
from .page import Page
from .utils.exceptions import SitemapException

class Sitemap(object):
    """Class responsible to get all posts from file.
    
    The main purpose is to walk the filesystem gathering all files that can be
    a post, generate Post instances and, on those that have 'tags' or 'category'
    headers, create lists of posts for any of them.
    """
    
    def __init__(self, path, extensions=(), encoding='utf-8'):
        self.path = path
        self.extensions = extensions
        self.encoding = encoding

    @property
    def pages(self):
        try:
            return self._pages
        except AttributeError:
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
                    pg = Page(filename, encoding=self.encoding, requires=('slug',))
                    if pg.meta['slug'] not in pagedict:
                        pagedict[pg.meta['slug']] = pg
                    else:
                        raise SitemapException('Slug "{0}" exists in the Sitemap.'.format(pg.meta['slug']))
                except Exception as e:
                    print('An exception occurred while processing the file "{0}": {1}. Ignoring file.'.format(filename, str(e)))
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
            #return {kw: p for kw, p in l.items() if item == p.meta[header] or (item in p.meta[header] and not isinstance(p.meta[header], str))}
    
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
    
    def __iter__(self):
        return compatibility.itervalues(self.pages)
