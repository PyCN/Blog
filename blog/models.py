# coding:utf-8
from django.db import models
from django.core.urlresolvers import reverse
from collections import defaultdict
from django.utils import timezone

from django.contrib.auth.models import User


# Create your models here.
class ArticleManage(models.Manager):

    def archive(self):
        date_list = Article.objects.datetimes(
            'created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)  # 模板不支持defaultdict


class Article(models.Model):
    # 'd':表示数据库的实际值;'Draft':表示模板列表中显示的值
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    objects = ArticleManage()

    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    last_modified_time = models.DateTimeField('修改时间', default=timezone.now)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    abstract = models.CharField(
        '摘要', max_length=54, blank=True, help_text="可选，如若为空将摘取正文的前54个字符")
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    user_likes = models.TextField('点赞用户', blank=True, default='')
    weight = models.PositiveIntegerField('权重', default=0)
    topped = models.BooleanField('置顶', default=False)
    attachment_url = models.CharField('附件地址', blank=True, default='', max_length=255)

    category = models.ForeignKey(
        'Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.abstract:
            if len(self.body) < 54:
                self.abstract = self.body
            else:
                self.abstract = self.body[:54]
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.pk})

    class Meta:
        ordering = ['-topped', '-created_time', '-last_modified_time']


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BlogComment(models.Model):
    # user_name = models.CharField('评论者名字', max_length=100)
    # user_email = models.EmailField('评论者邮箱', max_length=255)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    commentator = models.ForeignKey(
        User, verbose_name='用户', related_name='commentator', on_delete=models.CASCADE)
    article = models.ForeignKey(
        'Article', verbose_name='评论所属文章', related_name='comment', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.body[:20]


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=('用户'))
    phone = models.CharField(max_length=20)
    nickname = models.CharField(max_length=255)
    userimg = models.CharField('用户头像', default='', max_length='100')

class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
    describe = models.CharField('描述', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        permissions = (
            ('download_file', '下载附件'),
            ('upload_file', '上传附件'),
        )
'''    
class Search(models.Model):
    body_search = models.CharField(max_length=255) 
    
    def __unicode__(self):
        return self.body_search
'''
