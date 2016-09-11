#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

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
        self.body_with_53str = '12345678900987654321123456789009876543211234567890123'
        self.body_with_55str = '1234567890098765432112345678900987654321123456789012345'
        article1 = Article.objects.create(title='title1', body=self.body_with_53str,status='p')
        article2 = Article.objects.create(title='title2', body=self.body_with_55str,status='p', topped=True)
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
        self.assertEqual(response.context[2]['article_list'][0].abstract,self.body_with_55str[:54])
        self.assertEqual(response.context[2]['article_list'][2].abstract,self.body_with_53str)
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
        self.article2 = Article.objects.create(title='title2', body='article',status='d', category=self.category1)
        # 多对多的数据要用add添加
        self.article2.tags.add(tag1)
        self.article3 = Article.objects.create(title='title3', body=body_without_markdown, status='p', category=self.category1)
        self.article3.tags.add(tag1)
        self.article4 = Article.objects.create(title='title4', body='article', status='p')
    def test_get_object(self):
        response = self.client.get(reverse('blog:detail',args=(self.article1.id,)))
        self.assertContains(response,self.category1,status_code=200)
        response = self.client.get(reverse('blog:detail',args=(self.article2.id,)))
        self.assertContains(response, 'Page not found', status_code=404)
        # self.assertEqual(response.context_data['article'].body,[u'<pre><code>        ```python\n        def justcode(args):\n            if args:\n                print "Func has args"\n            else:\n                print "Func does\'t have args"\n        ```\n</code></pre>\n'])

    def test_get_context_data(self):
        response = self.client.get(reverse('blog:detail',args=(self.article1.id,)))
        self.assertQuerysetEqual(response.context_data['comment_list'],[])
        self.assertContains(response, u'我来评两句', status_code=200)
        

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
        
class ArchiveViewTests(TestCase):

    def setUp(self):
        article1 = Article.objects.create(title='title1', body='article',status='p')
        article2 = Article.objects.create(title='title2', body='article',status='d', topped=True)
        time_3  = timezone.now() - timezone.timedelta(seconds=20)
        article3 = Article.objects.create(title='title3', body='article',created_time=time_3,last_modified_time=time_3, status='p', topped=True)

    def test_get_queryset(self):
        '''
        测试未发表的文章是否会被过滤出来，且过滤出来的文章顺序是否正确
        '''
        response = self.client.get(reverse('blog:archive', args=(timezone.now().year, timezone.now().month,)))
        self.assertQuerysetEqual(response.context[2]['article_list'],['<Article: title1>','<Article: title3>'])

class CommentPostViewTests(TestCase):

    def setUp(self):
        category1 = Category.objects.create(name='category1')
        self.article1 = Article.objects.create(title='title1', body='article',status='p', category=category1)
        tag1 = Tag.objects.create(name='tag1')
        self.article1.tags.add(tag1)
        self.article2 = Article.objects.create(title='title2', body='article',status='d', category=category1)

        self.name = '1029645297@qq.com'
        self.password='password'
        user = User.objects.create_user(username=self.name, password=self.password)

    def test_form_valid_without_login(self):
        response = self.client.post((reverse('blog:comment', args=(self.article1.id,))), {'user_name':'111@qq.com', 'user_email':'111@qq.com', 'body':'111'}, follow=True)
        self.assertContains(response, '111@qq.com', status_code=200)

    def test_form_valid_with_login(self):
        self.assertTrue(self.client.login(username=self.name, password=self.password))
        response = self.client.post((reverse('blog:comment', args=(self.article1.id,))), {'user_name':'111@qq.com', 'user_email':'111@qq.com', 'body':'111'}, follow=True)
        self.assertContains(response, '111@qq.com', status_code=200)
        self.assertEqual(response.context[2]['comment_nums'], 1)

    def test_form_valid_without_published(self):
        response = self.client.post((reverse('blog:comment', args=(self.article2.id,))), {'user_name':'111@qq.com', 'user_email':'111@qq.com', 'body':'111'}, follow=True)
        self.assertEqual(response.redirect_chain[0], ('http://testserver/', 302))

    def test_form_invalid_without_login(self):
        response = self.client.post((reverse('blog:comment', args=(self.article1.id,))), {'user_name':'111@qq.com', 'user_email':'111', 'body':'111'}, follow=True)
        self.assertContains(response, u'0条评论', status_code=200)
        response = self.client.post((reverse('blog:comment', args=(self.article1.id,))), {'user_name':'111@qq.com', 'user_email':'111@qq.com', 'user_body':'111'}, follow=True)
        self.assertContains(response, u'0条评论', status_code=200)
        response = self.client.post((reverse('blog:comment', args=(self.article1.id,))), {'user_name':'111@qq.com', 'user_email':'111', 'body':'111', 'oter':'useless'}, follow=True)
        self.assertContains(response, u'0条评论', status_code=200)

    def test_form_invalid_with_login(self):
        self.assertTrue(self.client.login(username=self.name, password=self.password))
        response = self.client.post((reverse('blog:comment', args=(self.article1.id,))), {'user_name':'111@qq.com', 'user_email':'111', 'body':'111'}, follow=True)
        self.assertContains(response, u'0条评论', status_code=200)

    def test_form_invalid_without_published(self):
        response = self.client.post((reverse('blog:comment', args=(self.article2.id,))), {'user_name':'111@qq.com', 'user_email':'111', 'body':'111'}, follow=True)
        self.assertContains(response, u'0条评论', status_code=200)

class RegistTests(TestCase):

    def test_regist_with_get(self):
        response = self.client.get(reverse('blog:regist'))
        self.assertContains(response, u'确认密码', status_code=200)

    def test_regist_with_valid_form(self):
        response = self.client.post(reverse('blog:regist'), {'username':'111@qq.com', 'password1':'password', 'password2':'password', 'phone':'111'})
        self.assertEqual(response.context['regist_info'], u'注册成功')
        self.assertTrue(self.client.login(username='111@qq.com', password='password'))

    def test_regist_with_existed_account(self):
        user = User.objects.create_user(username='111@qq.com',password='111')
        response = self.client.post(reverse('blog:regist'), {'username':'111@qq.com', 'password1':'password', 'password2':'password', 'phone':'111'})
        self.assertContains(response, '111@qq.com')
        self.assertEqual(response.context['regist_info'], u'用户名已存在')

    def test_regist_with_different_password(self):
        response = self.client.post(reverse('blog:regist'), {'username':'111@qq.com', 'password1':'111', 'password2':'password', 'phone':'111'})
        self.assertContains(response, '111@qq.com')
        self.assertEqual(response.context['regist_info'], '两次输入的密码不一致!')

    def test_regist_with_invalid_form(self):
        response = self.client.post(reverse('blog:regist'), {'username':'111@qq.com', 'password1':'password', 'password':'password', 'phone':'111'})
        self.assertContains(response, '111@qq.com')
        self.assertEqual(response.context['regist_info'], 'input error')


class LogoutTests(TestCase):

    def test_logout_with_login(self):
        user = User.objects.create_user(username='111@qq.com',password='111')
        self.client.login(username='111@qq.com', password='111')
        response = self.client.get(reverse('blog:logout'), follow=True)
        self.assertEqual(response.redirect_chain, [('http://testserver/', 302)])

    def test_logout_without_login(self):
        response = self.client.get(reverse('blog:logout'), follow=True)
        self.assertEqual(response.redirect_chain, [('http://testserver/accounts/login/?next=/logout', 302)])

class RetrieveTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='111@qq.com',password='111') 
        user_profile = UserProfile()
        user_profile.user_id = user.id
        user_profile.phone = '111'
        user_profile.save()
        user = User.objects.create_user(username='222@qq.com',password='222') 

    def test_retrieve_with_get(self):
        response = self.client.get(reverse('blog:retrieve'))
        self.assertContains(response, u'修改密码', status_code=200)

    def test_retrieve_with_valid_form(self):
        response = self.client.post(reverse('blog:retrieve'), {'username':'111@qq.com', 'password1':'password', 'password2':'password', 'phone':'111'})
        self.assertEqual(response.context['retrieve_info'], u'密码修改成功')
        self.assertTrue(self.client.login(username='111@qq.com', password='password'))

    def test_retrieve_with_no_existed_account(self):
        response = self.client.post(reverse('blog:retrieve'), {'username':'333@qq.com', 'password1':'password', 'password2':'password', 'phone':'111'})
        self.assertContains(response, '333@qq.com')
        self.assertEqual(response.context['retrieve_info'], u'用户名不存在')

    def test_retrieve_with_different_password(self):
        response = self.client.post(reverse('blog:retrieve'), {'username':'111@qq.com', 'password1':'111', 'password2':'password', 'phone':'111'})
        self.assertContains(response, '111@qq.com')
        self.assertEqual(response.context['retrieve_info'], '两次输入的密码不一致!')

    def test_retrieve_with_no_phone_account(self):
        response = self.client.post(reverse('blog:retrieve'), {'username':'222@qq.com', 'password1':'password', 'password2':'password', 'phone':'222'})
        self.assertContains(response, '222@qq.com')
        self.assertEqual(response.context['retrieve_info'], u'该用户不可修改密码')

    def test_retrieve_with_wrong_phone(self):
        response = self.client.post(reverse('blog:retrieve'), {'username':'111@qq.com', 'password1':'111', 'password2':'password', 'phone':'222'}) 
        self.assertContains(response, '111@qq.com')
        self.assertEqual(response.context['retrieve_info'], '手机号有误')

    def test_retrieve_with_invalid_form(self):
        response = self.client.post(reverse('blog:retrieve'), {'username':'111@qq.com', 'password1':'password', 'password':'password', 'phone':'111'})
        self.assertContains(response, '111@qq.com')
        self.assertEqual(response.context['retrieve_info'], 'input error')


class GenerateQrcodeTests(TestCase):

    def test_qrcode_with_get(self):
        response = self.client.get(reverse('blog:qrcode'), follow=True)
        self.assertEqual(response.redirect_chain, [('http://testserver/', 302)])

    def test_qrcode_without_target_url(self):
        response = self.client.post(reverse('blog:qrcode'), follow=True)
        self.assertEqual(response.redirect_chain, [('http://testserver/', 302)])

    def test_qrcode_with_none_target_url(self):
        response = self.client.post(reverse('blog:qrcode'), {'target_url':'www.baidu.com'}, follow=True)
        self.assertEqual(response.status_code, 200)



