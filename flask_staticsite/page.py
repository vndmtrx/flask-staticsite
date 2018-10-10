#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml, os

class PageException(Exception):
    """
    Exception crafted to be raised by Page Class and needs to be catched
    elsewhere.
    """

def _preload_header(file, encoding, shield='---'):
    header = {}
    try:
        with open(file) as raw:
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
                raise PageException('Malformed header')
            header['headers'] = yaml.safe_load(s)
    except IOError:
        print('Could not read file {0}'.format(file))
        pass
    return header

class Page(object):
    """Simple class to store all information regarding a static page.
    
    The main purpose is to process file headers and if all required readers
    are present, proceed with object creation. Also, load file contents and
    deliver them.
    """
    
    def __new__(cls, path, encoding='utf-8', requires=()):
        yml = _preload_header(path, encoding)
        if len(yml) == 2:
            obj = super(Page, cls).__new__(cls)
            obj._meta = yml['headers']
            obj._filepos = yml['filepos']
            req = ('slug',) + requires
            for item in req:
                if item not in obj._meta:
                    raise PageException('Required header is not present in file "{0}": "{1}"'.format(path, item))
            return obj
        else:
            raise PageException('File "{0}" has no headers'.format(path))
    
    
    def __init__(self, path, encoding='utf-8', requires=()):
        self.path = path
        self.encoding = encoding
        self.mtime = os.path.getmtime(path)
    
    def __repr__(self):
        return '<Page "{0}">'.format(self.path)
    
    @property
    def meta(self):
        return self._meta
    
    @property
    def content(self):
        try:
            return self._content
        except AttributeError:
            if self.mtime != os.path.getmtime(self.path):
                raise PageException('File "{0}" changed since instance creation'.format(self.path))
            with open(self.path) as raw:
                raw.seek(self._filepos, 0)
                self._content = raw.read().strip()
            return self._content
