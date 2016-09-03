#coding:utf-8

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

try:
    import pytz
except:
    pass

from models import Article, Category, Tag, BlogComment, UserProfile

def create_article():
    # time_2011_8 = datetime.datetime(2011, 8, 22, 11, 23, 45, 564, tzinfo=pytz.utc)
    # article2 = Article.objects.create(title='title2', body='article',created_time=time_2011_8,\
    pass

class IndexViewTests(TestCase):
    def test_get_queryset_with_topped(self):
        '''
        if articles contains topped and untopped, the topped one should be first.
        '''
        response = self.client.get('/')
        self.assertQuerysetEqual(response.context[2]['article_list'],[])

