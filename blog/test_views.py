#coding:utf-8

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

try:
    import pytz
except:
    pass

from models import Article, ArticleManage, Category, Tag, BlogComment, UserProfile

def create_article():
    # time_2011_8 = datetime.datetime(2011, 8, 22, 11, 23, 45, 564, tzinfo=pytz.utc)
    # article2 = Article.objects.create(title='title2', body='article',created_time=time_2011_8,\
    pass

class IndexViewTests(TestCase):
    def test_get_queryset_with_topped(self):
        '''
        if articles contains topped and untopped, the topped one should be first.
        '''
        article1 = Article.objects.create(title='title1', body='article',status='p')
        time_now = timezone.now()
        article1 = Article.objects.create(title='title1', body='article',created_time=time_now,\
                                          last_modified_time=time_now, status='p')
        response = self.client.get(reverse('blog:index'))
        article_list = Article.objects.all()
        print article_list
        print response.context
        self.assertQuerysetEqual(response.context[2]['article_list'],['1'])

    def test_get_queryset_with_order(self):
        article2 = Article.objects.create(title='title2', body='article',status='Published')
        response = self.client.get('/')
        article_list = Article.objects.all()
        print article_list
        self.assertQuerysetEqual(response.context,['d'])        
