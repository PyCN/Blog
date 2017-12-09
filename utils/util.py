# coding:utf-8

import logging
import time
import functools

logger = logging.getLogger('web')


# 字符串转时间戳
def str2timestamp(d, f="%Y-%m-%d %H:%M:%S"):
    t = time.strptime(d, f)
    return time.mktime(t)


# 时间戳转字符串
def timestamp2str(d, f="%Y-%m-%d %H:%M:%S"):
    x = time.localtime(d)
    return time.strftime(f, x)


def runTime(func):
    logger = logging.getLogger('web')

    @functools.wraps(func)
    def wrapper(*args, **kw):
        time1 = time.time()
        result = func(*args, **kw)
        run_time = time.time() - time1
        logger.info('%s run time: %f' %
                    (func.__name__, run_time))
        return result
    return wrapper


def alwaysLog(func):
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


def safeInt(num):
    """return None if num is not a number"""
    try:
        num = int(num)
    except Exception:
        return None
    return num
