#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

IS_PY3 = sys.version_info[0] == 3
string_types = (str, ) if IS_PY3 else (basestring, )
text_type = str if IS_PY3 else unicode


def itervalues(obj, **kwargs):
    return iter(obj.values(**kwargs)) if IS_PY3 else obj.itervalues(**kwargs)
