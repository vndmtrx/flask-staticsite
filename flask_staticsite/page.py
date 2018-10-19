#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import six
import yaml
import logging
from io import open
from .utils.exceptions import PageException

logger = logging.getLogger(__name__)

def _preload_header(file, encoding, shield='---'):
    header = {}
    with open(file, encoding=encoding) as raw:
        s = ''
        r = raw.readline().strip()
        if r == shield:
            while True:
                line = raw.readline()
                if not line:
                    break
                elif line.strip() != shield:
                    s += line
                else:
                    header['filepos'] = raw.tell()
                    break
        if 'filepos' not in header:
            raise PageException('Malformed header in file: {0}'.format(file))
        header['headers'] = yaml.safe_load(s)
    return header

class Page(object):
    """Simple class to store all information regarding a static page.
    
    The main purpose is to process file headers and if all required readers
    are present, proceed with object creation. Also, load file contents and
    deliver them.
    """
    
    def __new__(cls, filename, encoding='utf-8', keymap_strategy='{filename}', requires=[]):
        yml = _preload_header(filename, encoding)
        #if 'headers' in yml and 'filepos' in yml:
        #if all(x in yml for x in ('headers','filepos')):
        if {'headers', 'filepos'}.issubset(yml):
            obj = super(Page, cls).__new__(cls)
            obj._meta = yml['headers']
            obj._meta['filename'] = filename
            obj._filepos = yml['filepos']
            for item in requires:
                if item not in obj._meta:
                    raise PageException('Required header is not present in file "{0}": "{1}"'.format(filename, item))
            return obj
        else:
            raise PageException('No headers found in file: {0}'.format(filename))
    
    
    def __init__(self, filename, encoding, keymap_strategy, requires):
        self.encoding = encoding
        self.keymap_strategy = keymap_strategy
        self.mtime = os.path.getmtime(filename)
    
    def __repr__(self):
        return '<Page "{0}">'.format(self.meta['filename'])
    
    @property
    def key(self):
        """
        Call a function or uses a string formatting to return the object key.
        Examples:
        '{category}/{slug}'
        def dateslug(meta):
            parse_time='%Y-%m-%d %H:%M %z'
            format_time='%Y/%m'
            if isinstance(meta['date'], datetime.date):
                dt = meta['date']
            else:
                from datetime import datetime
                dt = datetime.datetime.strptime(meta['date'], parse_ptime)
            return '{0}/{1}'.format(dt.strftime(format_time), meta['slug'])
        """
        kst = self.keymap_strategy
        return kst(self.meta) if callable(kst) else kst.format_map(self.meta)
    
    @property
    def meta(self):
        return self._meta
    
    @property
    def content(self):
        try:
            return self._content
        except AttributeError:
            if self.mtime != os.path.getmtime(self.meta['filename']):
                raise PageException('File changed since instance creation: {0}'.format(self.meta['filename']))
            with open(self.meta['filename'], encoding=self.encoding) as raw:
                raw.seek(self._filepos, 0)
                self._content = raw.read().strip()
            return self._content
