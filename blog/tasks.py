from __future__ import absolute_import, unicode_literals

import urllib2
import json
import logging

from celery import shared_task
from blog.models import Article, Category, Tag, BlogComment, UserProfile, VisitorIP

IP_INFO_URL = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='
@shared_task
def add(x, y):
    return x + y

@shared_task
def save_client_ip(client_ip):
    country = ''
    city = ''
    ip_info = ''
    last_ip = VisitorIP.objects.last()
    if not last_ip or last_ip == client_ip:
        url = IP_INFO_URL + client_ip
        try:
            ip_info = urllib2.urlopen(url)
            ip_info = ip_info.read()
        except Exception, e:
            logging.warn(url)
            logging.info('Get ip info failed: %s' % e)
        if ip_info:
            ip_info = json.loads(ip_info)
            country = ip_info['country'].encode('utf-8')
            city = ip_info['city'].encode('utf-8')

        VisitorIP.objects.create(ip=client_ip, country=country, city=city)
    else:
        pass
