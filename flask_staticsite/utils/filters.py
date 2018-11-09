#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PageFilter(list):
    def filter(self, header, item=None):
        def _apply():
            filtered_pages = (p for p in self if header in p.headers)
            for p in filtered_pages:
                if isinstance(p.headers[header], (list, dict, tuple, set)):
                    if item not in p.headers[header]:
                        continue
                elif item != p.headers[header]:
                    continue
                yield p
        return PageFilter(list(_apply()))
    
    def sort(self, header, reverse=False):
        filtered_pages = (p for p in self if header in p.headers)
        return PageFilter(sorted(self, key=lambda k: k.headers[header], reverse=reverse))
    
    def __repr__(self):
        return '<PageFilter [{0}]>'.format(', '.join(map(str, self)))
