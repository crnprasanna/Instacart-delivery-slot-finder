#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Timeout helper module
'''

from functools import wraps
import sys
import timeout_decorator
import time

# Timeout exception for linux only

DEFAULT_TIMEOUT = 120


def custom_decorator(f):

    @wraps(f)
    def wrapped(*args, **kwargs):
        if sys.platform != 'win32':

            @timeout_decorator.timeout(DEFAULT_TIMEOUT)
            def tmp(f):
                return f(*args, **kwargs)
            r = tmp(f)
        else:
            r = f(*args, **kwargs)
        return r
    return wrapped


@custom_decorator
def myfunc(sleep_time=6):
    print('Test function started')
    time.sleep(sleep_time)
    print('Test function completed')

if __name__ == '__main__':
    myfunc()  # won't raise exception
    myfunc(200)  # will raise exception
