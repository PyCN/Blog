# coding:utf-8

from __future__ import absolute_import, unicode_literals

import urllib2
import json
import logging

from django.core.cache import cache
from celery import shared_task
from blog.models import Article, Category, Tag, BlogComment, UserProfile, VisitorIP
from blog_project import settings

IP_INFO_URL = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='


@shared_task
def add(x, y):
    return x + y


# TODO 检查文章id判断是否为同一次访问
@shared_task
def save_client_ip(client_ip, article=None):
    country = ''
    city = ''
    ip_info = ''
    visitor_num = cache.get('visitor_num')
    if not visitor_num:
        visitor_num = VisitorIP.objects.count()
        cache.set('visitor_num', visitor_num, settings.REDIS_TIMEOUT)
    last_ip = VisitorIP.objects.first()
    if not last_ip or last_ip.ip != client_ip:
        url = IP_INFO_URL + client_ip
        try:
            ip_info = urllib2.urlopen(url)
            ip_info = ip_info.read()
        except Exception, e:
            logging.info(url)
            logging.error('Get ip info failed: %s' % e)
        if ip_info:
            ip_info = json.loads(ip_info)
            country = ip_info['country'].encode('utf-8')
            if ip_info.has_key('city') and ip_info['city']:
                city = ip_info['city'].encode('utf-8')
            else:
                city = country
    else:
        return 'existed ip'
    if article:
        article = Article.objects.get(id=article)
    VisitorIP.objects.create(ip=client_ip, country=country, city=city,
                             article=article)
    cache.set('visitor_num', visitor_num + 1, settings.REDIS_TIMEOUT)
