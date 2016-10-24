# coding:utf-8

from django.conf.urls import url
from blog import views
from django.views.decorators.cache import cache_page  # 缓存

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^qrcode$', views.generate_qrcode, name='qrcode'),
    # 如果用 r'^article/(?P<article_id>\d+)'，则文章无法评论
    url(r'^article/(?P<article_id>\d+)$',
        views.ArticleDetailView.as_view(), name='detail'),
    url(r'^category/(?P<cate_id>\d+)$',
        views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$',
        views.ArchiveView.as_view(), name='archive'),
    url(r'^article/(?P<article_id>\d+)/comment/$',
        views.CommentPostView.as_view(), name='comment'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^account$', views.AccountView.as_view(), name='account'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^regist$', cache_page(60)(views.regist), name='regist'),
    url(r'^retrieve$', views.retrieve, name='retrieve'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'blog/login.html'}),
]
