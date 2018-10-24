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
    header = None
    filepos = None
    s = ''
    with open(file, encoding=encoding) as raw:
        r = raw.readline().strip()
        if r == shield:
            while True:
                line = raw.readline()
                if not line:
                    break
                elif line.strip() == shield:
                    filepos = raw.tell()
                    break
                else:
                    s += line
        if filepos == None:
            raise PageException('Malformed header in file: {0}'.format(file))
        header = yaml.safe_load(s)
    return filepos, header

class Page(object):
    """Simple class to store all information regarding a static page.
    
    The main purpose is to process file headers and if all required readers
    are present, proceed with object creation. Also, load file contents and
    deliver them.
    """
    
    def __new__(cls, filename, encoding='utf-8', keymap_strategy='{filename}'):
        filepos, yml = _preload_header(filename, encoding)
        if filepos and yml:
            obj = super(Page, cls).__new__(cls)
            obj._meta = yml
            obj._meta['filename'] = filename
            obj._filepos = filepos
            return obj
        else:
            raise PageException('No headers found in file: {0}'.format(filename))
    
    
    def __init__(self, filename, encoding='utf-8', keymap_strategy='{filename}'):
        self.encoding = encoding
        self.keymap_strategy = keymap_strategy
        self.mtime = os.path.getmtime(filename)
    
    def __repr__(self):
        return '<Page "{0}">'.format(self.key)
    
    @property
    def key(self):
        """
        Call a function or uses a string formatting to return the object key.
        Examples:
        
        '{category}/{slug}'
        
        import datetime
        def dateslug(meta):
            parse_time='%Y-%m-%d %H:%M %z'
            format_time='%Y/%m'
            if isinstance(meta['date'], datetime.date):
                dt = meta['date']
            else:
                dt = datetime.datetime.strptime(meta['date'], parse_time)
            return '{0}/{1}'.format(dt.strftime(format_time), meta['slug'])
        """
        kst = self.keymap_strategy
        return kst(self.headers) if callable(kst) else kst.format_map(self.headers)
    
    @property
    def headers(self):
        return self._meta
    
    def __getitem__(self, name):
        """Shortcut for accessing metadata.
        ``page['slug']`` or, in a template, ``{{ page.slug }}`` are
        equivalent to ``page.headers['slug']``.
        """
        return self.headers[name]
    
    @property
    def content(self):
        try:
            return self._content
        except AttributeError:
            if self.mtime != os.path.getmtime(self.headers['filename']):
                raise PageException('File changed since instance creation: {0}'.format(self.headers['filename']))
            with open(self.headers['filename'], encoding=self.encoding) as raw:
                raw.seek(self._filepos, 0)
                self._content = raw.read().strip()
            return self._content
