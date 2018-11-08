#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultPaginator(object):
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
    
    def __repr__(self):
        return '<DefaultPaginator [{0}]>'.format(', '.join(map(str, self._paginated_list())))
