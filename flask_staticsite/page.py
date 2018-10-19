#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import six
import yaml
import logging
from .utils.exceptions import PageException
from .utils.key_mappers import SlugMapper

logger = logging.getLogger(__name__)

def _preload_header(file, encoding, shield='---'):
    header = {}
    with open(file, encoding=encoding) if six.PY3 else open(file) as raw:
        s = ''
        r = raw.readline().strip() if six.PY3 else raw.readline().decode(encoding).strip()
        if r == shield:
            while True:
                line = raw.readline() if six.PY3 else raw.readline().decode(encoding)
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
    
    def __new__(cls, filename, encoding='utf-8', key_mapper=SlugMapper()):
        yml = _preload_header(filename, encoding)
        #if 'headers' in yml and 'filepos' in yml:
        #if all(x in yml for x in ('headers','filepos')):
        if {'headers', 'filepos'}.issubset(yml):
            obj = super(Page, cls).__new__(cls)
            obj._meta = yml['headers']
            obj._filepos = yml['filepos']
            for item in key_mapper.requires:
                if item not in obj._meta:
                    raise PageException('Required header is not present in file "{0}": "{1}"'.format(filename, item))
            return obj
        else:
            raise PageException('No headers found in file: {0}'.format(filename))
    
    
    def __init__(self, filename, encoding, key_mapper):
        self.filename = filename
        self.encoding = encoding
        self.key_mapper=key_mapper
        self.mtime = os.path.getmtime(filename)
    
    def __repr__(self):
        return '<Page "{0}">'.format(self.filename)
    
    @property
    def key(self):
        return self.key_mapper.get_key(self)
    
    @property
    def meta(self):
        return self._meta
    
    @property
    def content(self):
        try:
            return self._content
        except AttributeError:
            if self.mtime != os.path.getmtime(self.filename):
                raise PageException('File changed since instance creation: {0}'.format(self.filename))
            with open(self.filename, encoding=self.encoding) if compatibility.IS_PY3 else open(self.filename) as raw:
                raw.seek(self._filepos, 0)
                self._content = raw.read().strip() if compatibility.IS_PY3 else raw.read().decode(encoding).strip()
            return self._content
