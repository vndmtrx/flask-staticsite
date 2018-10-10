#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml, os

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
                raise ValueError('Malformed header')
            header['headers'] = yaml.safe_load(s)
    except IOError:
        print('Could not read file {0}'.format(file))
        pass
    return header

class Page(object):
    def __new__(cls, path, encoding='utf-8', requires=()):
        yml = _preload_header(path, encoding)
        if len(yml) == 2:
            obj = super(Page, cls).__new__(cls)
            obj.meta = yml['headers']
            obj._filepos = yml['filepos']
            for req in requires:
                if req not in obj.meta:
                    raise ValueError('Required headers aren''t present')
            return obj
        else:
            raise ValueError('File has no headers')
    
    
    def __init__(self, path, encoding='utf-8', requires=()):
        self.path = path
        self.encoding = encoding
        self.mtime = os.path.getmtime(path)
