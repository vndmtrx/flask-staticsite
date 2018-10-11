#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from . import compatibility
from .page import Page

class Sitemaps(object):
    """Class responsible to get all posts from file.
    
    The main purpose is to walk the filesystem gathering all files that can be
    a post, generate Post instances and, on those that have 'tags' or 'category'
    headers, create lists of posts for any of them.
    """
    
    def __init__(self, path, extensions):
        self.path = path
        self.extensions = extensions

    @property
    def pages(self):
        try:
            return self._pages
        except AttributeError:
            def _walker():
                for cur_path, _, filenames in os.walk(self.path):
                    rel_path = cur_path.replace(self.path, '').lstrip(os.sep)
                    path_prefix = tuple(rel_path.split(os.sep)) if rel_path else ()
                    
                    for n in filenames:
                        if not n.endswith(self.extension):
                            continue
                        
                        full_name = os.path.join(cur_path, name)
                        yield full_name
    
    @property
    def tags(self):
        pass
    
    @property
    def categories(self):
        pass
    
    def __iter__(self):
        return compatibility.itervalues(self.pages)
