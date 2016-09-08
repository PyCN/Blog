#coding=utf-8

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
    
    def setUp(self):
        article1 = Article.objects.create(title='title1', body='article',status='p')
        article2 = Article.objects.create(title='title2', body='article',status='p', topped=True)
        time_3  = timezone.now() - timezone.timedelta(seconds=20)
        article3 = Article.objects.create(title='title3', body='article',created_time=time_3,last_modified_time=time_3, status='p', topped=True)
        time_4 = timezone.now() - timezone.timedelta(seconds=30)
        article4 = Article.objects.create(title='title4', body='article',created_time=time_3,last_modified_time=time_4, status='p')
        article5 = Article.objects.create(title='title5', body='article',created_time=time_3,last_modified_time=time_3, status='p')
        article6 = Article.objects.create(title='title6', body='article',status='d')
        
    def test_get_queryset_with_topped(self):
        '''
        if articles contains topped and untopped, the topped one should be first, then by created_time, last_modified_time.
        '''
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context[2]['article_list'],['<Article: title2>', '<Article: title3>','<Article: title1>', '<Article: title5>','<Article: title4>',])

    def test_get_context_data(self):
        response = self.client.get(reverse('blog:index'))
        time_now = timezone.now()
        self.assertQuerysetEqual(response.context[1]['date_archive'],['(%s, [%s])' % (time_now.year, time_now.month)])
        
class ArticleDetaiilViewTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        tag1 = Tag.objects.create(name='tag1')
        body_with_markdown = '''
        
            ```python
            def justcode(args):
                if args:
                    print "Func has args"
                else:
                    print "Func does't have args"
            ```
            
        '''
        body_without_markdown = '''
            def justcode(args):
                if args:
                    print "Func has args"
                else:
                    print "Func does't have args"
        '''
        self.article1 = Article.objects.create(title='title1', body=body_with_markdown, status='p', category=self.category1)
        self.article2 = Article.objects.create(title='title2', body='article',status='p')
        # 多对多的数据要用add添加
        self.article2.tags.add(tag1)
        self.article3 = Article.objects.create(title='title3', body=body_without_markdown, status='p', category=self.category1)
        self.article3.tags.add(tag1)
        self.article4 = Article.objects.create(title='title4', body='article', status='p')
    def test_get_object(self):
        response = self.client.get(reverse('blog:detail',args=(self.article1.id,)))
        self.assertContains(response,self.category1,status_code=200)
        # self.assertEqual(response.context_data['article'].body,[u'<pre><code>        ```python\n        def justcode(args):\n            if args:\n                print "Func has args"\n            else:\n                print "Func does\'t have args"\n        ```\n</code></pre>\n'])

    def test_get_context_data(self):
        response = self.client.get(reverse('blog:detail',args=(self.article1.id,)))
        self.assertQuerysetEqual(response.context_data['comment_list'],[])
        print response.context_data['form']

class CategoryViewTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.article1 = Article.objects.create(title='title1', body='body', status='p', category=self.category1)
        self.article2 = Article.objects.create(title='title2', body='body', status='p', category=self.category1)
        self.category2 = Category.objects.create(name='another_category2')
    

    def test_get_queryset(self):
        response = self.client.get(reverse('blog:category',args=(self.category1.id,)))
        self.assertQuerysetEqual(response.context[1]['article_list'],['<Article: title2>', '<Article: title1>']) 
        response = self.client.get(reverse('blog:category',args=(self.category2.id,)))
        self.assertQuerysetEqual(response.context[1]['article_list'],[]) 

    def test_get_context_data(self):
        response = self.client.get(reverse('blog:category',args=(self.category2.id,)))
        self.assertQuerysetEqual(response.context_data['category_list'],['<Category: another_category2>', '<Category: category1>'])

class TarviewTests(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')
        self.tag4 = Tag.objects.create(name='tag4')
        self.article1 = Article.objects.create(title='title1', body='body', status='p')
        self.article2 = Article.objects.create(title='title2', body='body', status='p')
        self.article3 = Article.objects.create(title='title3', body='body', status='d')
        self.article1.tags.add(self.tag1)
        self.article1.tags.add(self.tag4)
        self.article2.tags.add(self.tag2)
        self.article3.tags.add(self.tag3)
    

    def test_get_queryset(self):
        response = self.client.get(reverse('blog:tag',args=(self.tag1.id,)))
        self.assertQuerysetEqual(response.context[1]['article_list'],['<Article: title1>']) 
        response = self.client.get(reverse('blog:tag',args=(self.tag4.id,)))
        self.assertQuerysetEqual(response.context[1]['article_list'],['<Article: title1>']) 
        response = self.client.get(reverse('blog:tag',args=(self.tag2.id,)))
        self.assertQuerysetEqual(response.context[1]['article_list'],['<Article: title2>']) 
        response = self.client.get(reverse('blog:tag',args=(self.tag3.id,)))
        self.assertQuerysetEqual(response.context[1]['article_list'],[]) 

    def test_get_context_data(self):
        response = self.client.get(reverse('blog:tag',args=(self.tag2.id,)))
        self.assertQuerysetEqual(response.context_data['tag_list'],['<Tag: tag1>', '<Tag: tag2>', '<Tag: tag3>', '<Tag: tag4>'])
