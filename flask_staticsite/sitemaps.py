#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from . import compatibility
from .page import Page

class Paginator(object):
    """
    Class responsible to paginate post lists to use in indexes pages.
    """
    
    def __init__(self, list, offset):
        self._list = list
        self._offset = offset
    
    def _paginated_list(self):
        return [self._list[i:i + self._offset] for i in range(0, len(self._list), self._offset)]
    
    def __getitem__(self, idx):
        return self._paginated_list()[idx]
    
    def __len__(self):
        return len(self._paginated_list())
    
    def __iter__(self):
        return iter(self._paginated_list())

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
