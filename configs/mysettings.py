#coding:utf-8
"""
Django settings for blog_project project.

It only contains database settings.
"""

DEBUG = True 
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '120.24.191.19', 'cblog.xyz',
                 'www.cblog.xyz', '192.168.0.195', 'master']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Blog',
        'USER': 'ctg',
        'PASSWORD': '1094760953',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
