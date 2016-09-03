#coding:utf-8
import datetime
try:
    import pytz
except:
    pass
from django.utils import timezone
from django.test import TestCase

from models import Article, Category, Tag, BlogComment, UserProfile

class ArticleTests(TestCase):
    def test_manage_archive(self):
        '''
        get_absolute_url() should return right url
        '''
        time_now = timezone.now()
        try:
            time_2011_8 = datetime.datetime(2011, 8, 22, 11, 23, 45, 564, tzinfo=pytz.utc)
            time_2015_6 = datetime.datetime(2015, 6, 22, 11, 23, 45, 564, tzinfo=pytz.utc)
            time_2015_8 = datetime.datetime(2015, 8, 22, 11, 23, 45, 564, tzinfo=pytz.timezone("Asia/Shanghai"))
        except:
            time_2011_8 = datetime.datetime(2011, 8, 22, 11, 23, 45, 564)
            time_2015_6 = datetime.datetime(2015, 6, 22, 11, 23, 45, 564)
            time_2015_8 = datetime.datetime(2015, 8, 22, 11, 23, 45, 564)
        article1 = Article.objects.create(title='title1', body='article',created_time=time_now,\
                                          last_modified_time=time_now, status='Published')
        article2 = Article.objects.create(title='title2', body='article',created_time=time_2011_8,\
                                          last_modified_time=time_2011_8, status='Published')
        article3 = Article.objects.create(title='title3', body='article',created_time=time_2015_8,\
                                          last_modified_time=time_2015_8, status='Published')
        article1 = Article.objects.create(title='title1', body='article',created_time=time_2015_6,\
                                          last_modified_time=time_2015_6, status='Published')
        self.assertEqual(Article.objects.archive(),[(time_now.year, [time_now.month]), (2015, [8, 6]), (2011, [8])])
        
        
class CategoryTests(TestCase):
    
    def test_name(self):
        category1 = Category('category','1212')
        self.assertEqual(category1.pk, 'category')
        self.assertEqual(category1.name, '1212')
    
