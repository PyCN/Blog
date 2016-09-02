#coding:utf-8

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Article, Category, Tag, BlogComment, UserProfile

class ArticleTests(TestCase):
    def test_was_right_url(self):
        '''
        get_absolute_url() should return right url
        '''
        time_create = timezone.now()
        article1 = Article('title','article',time_create,time_create,'Published')
        self.assertEqual(article1.get_absolute_url(), '/1')
        self.assertEqual(article1.id, 'title')
        
        
class CategoryTests(TestCase):
    
    def test_name(self):
        category1 = Category('category','1212')
        self.assertEqual(category1.pk, 'category')
        self.assertEqual(category1.name, '1212')
    