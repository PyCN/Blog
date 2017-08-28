from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    url(r'^tag/$', TagView.as_view(), name='tag'),
    url(r'^link/$', LinkView.as_view(), name='link'),
    url(r'^users/$', UsersView.as_view(), name='users'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^visitor/$', VisitorListView.as_view(), name='visitor'),
    url(r'^upload/$', csrf_exempt(UploadView.as_view()), name='upload'),
    url(r'^categories/$', CategoryView.as_view(), name='categories'),
    url(r'^article/add/$', ArticleAddView.as_view(), name='article-add'),
    url(r'^article/list/$', ArticleListView.as_view(), name='article-list'),
    url(r'^article/edit/$', ArticleEditView.as_view(), name='article-edit'),
    url(r'^article/body/$', ArticleBodyView.as_view(), name='article-body'),
    url(r'^message/os/$', MessageOSView.as_view(), name='message-os'),
    url(r'^message/comment/$', MessageCommentView.as_view(), name='message-comment'),
    url(r'^$', DashboardView.as_view(), name='dashboard'),
]
