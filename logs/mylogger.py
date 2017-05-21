# coding:utf-8

import logging
import functools


logger = logging.getLogger(__name__)


def myLog(func):
    '''Log exception message when func run error
    Remember, this func only use to decorate simple func'''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            result = func(*args, **kw)
        except Exception, e:
            logger.exception(e)
        return result
    return wrapper
