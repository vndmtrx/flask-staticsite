#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml, os

from . import compatibility

class PageException(Exception):
    """
    Exception crafted to be raised by Page Class and needs to be catched
    elsewhere.
    """

def _preload_header(file, encoding, shield='---'):
    header = {}
    with open(file, encoding=encoding) if compatibility.IS_PY3 else open(file) as raw:
        s = ''
        r = raw.readline().strip() if compatibility.IS_PY3 else raw.readline().decode(encoding).strip()
        if r == shield:
            while True:
                line = raw.readline() if compatibility.IS_PY3 else raw.readline().decode(encoding)
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
    
    def __new__(cls, filename, encoding='utf-8', requires=()):
        yml = _preload_header(filename, encoding)
        #if 'headers' in yml and 'filepos' in yml:
        #if all(x in yml for x in ('headers','filepos')):
        if {'headers', 'filepos'}.issubset(yml):
            obj = super(Page, cls).__new__(cls)
            obj._meta = yml['headers']
            obj._filepos = yml['filepos']
            for item in requires:
                if item not in obj._meta:
                    raise PageException('Required header is not present in file "{0}": "{1}"'.format(filename, item))
            return obj
        else:
            raise PageException('No headers found in file: {0}'.format(filename))
    
    
    def __init__(self, filename, encoding='utf-8', requires=()):
        self.filename = filename
        self.encoding = encoding
        self.mtime = os.path.getmtime(filename)
    
    def __repr__(self):
        return '<Page "{0}">'.format(self.filename)
    
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
