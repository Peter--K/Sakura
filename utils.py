#!/usr/bin/env python

# Copyright (c) 2013-2014 Synchrotron Light Source Australia Pty Ltd.
# Released under the Modified BSD license
# See LICENSE

import functools
def memoize(obj):
    """Memoization decorator from the PythonDecoratorLibrary
    http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer
