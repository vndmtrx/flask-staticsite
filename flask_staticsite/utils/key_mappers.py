#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from ..page import Page

class SlugMapper(object):
    def __init__(self):
        self.requires = ('slug',)
    
    def get_key(self, page):
        return page.meta['slug']


class FilenameMapper(object):
    def __init__(self):
        self.requires = ()
    
    def get_key(self, page):
        return page.filename


class CategorySlugMapper(object):
    def __init__(self):
        self.requires = ('slug', 'category')
    
    def get_key(self, page):
        return '{0}/{1}'.format(page.meta['category'], page.meta['slug'])


class DateSlugMapper(object):
    def __init__(self, ptime='%Y-%m-%d %H:%M %z', ftime='%Y/%m'):
        self.requires = ('slug', 'date')
        self.ptime = ptime
        self.ftime = ftime

    def get_key(self, page):
        if isinstance(page.meta['date'], datetime.date):
            dt = page.meta['date']
        else:
            dt = datetime.datetime.strptime(page.meta['date'], self.ptime)
        return '{0}/{1}'.format(dt.strftime(self.ftime), page.meta['slug'])
