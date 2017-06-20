# coding:utf-8

import json
import logging

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView, FormView
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings

from .forms import LinkForm, SettingForm
from blog.models import Article, BlogComment, Category, Permission,\
        Link, Tag, UserProfile, UserProfile
from .models import *
from logs.mylogger import myLog
# from users.models import *
from utils.mixin_utils import LoginRequiredMixin

__all__ = [
    'ArticleAddView',
    'ArticleListView',
    'ArticleEditView',
    'ArticleBodyView',
    'TagView',
    'CategoryView',
    'UploadView',
    'LinkView',
    'UsersView',
    'ProfileView',
    'DashboardView',
    'MessageOSView',
    'MessageCommentView',
    'SettingView'
]


logger = logging.getLogger(__name__)

# Create your views here.


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/dashboard.html')


class ArticleAddView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all().values('name')
        tags = Tag.objects.all().values('name')
        return render(request, 'admin/article-add.html', {'categories': categories, 'tags': tags})

    def post(self, request):
        d = dict(request.POST)
        title = d['title'][0]
        status = d['status'][0]
        topped = d['topped'][0]
        if topped == '1':
            topped = True
        else:
            topped = False
        abstract = d.get('abstract', [None])[0]
        editormd = d['editormd-markdown-doc'][0]
        tags = d.get('tags', '')
        categories = d.get('categories', [''])[0]
        try:
            aid = d['id'][0]
            article = Article.objects.get(pk=aid)
            article.title = title
            article.body = editormd
            article.status = status
            article.topped = topped
            article.abstract = abstract
            article.views = d['views'][0]
            exist_tag = d['exist_tag'][0].split(',')
            old_tag = article.get_tag().strip(',').split(',')
            tags = list(set(tags).difference(set(exist_tag)))
            delete_tag_list = list(set(old_tag).difference(set(exist_tag)))
            for dt in delete_tag_list:
                t = Tag.objects.get(name=dt)
                article.tags.remove(t)
        except Exception:
            category = Category.objects.get(name=categories)
            article = Article.objects.create(
                title=title, body=editormd, status=status, abstract=abstract,
                category=category, topped=topped)
        if tags:
            for tag in tags:
                t = Tag.objects.get(name=tag)
                article.tags.add(t)
        if categories:
            article.category = Category.objects.get(name=categories)
        article.save()
        return HttpResponseRedirect(reverse('admin:article-list'))

    def delete(self, request):
        logger.info('delete article')
        try:
            data = json.loads(request.body)
            article = Article.objects.get(pk=data['id'])
            aid = article.id
            article.delete()
        except Exception, e:
            logger.error(e)
        return HttpResponse(json.dumps({'aid': aid}))


class ArticleEditView(LoginRequiredMixin, View):
    def get(self, request):
        aid = request.GET.get('aid', '')
        if aid:
            article = Article.objects.get(pk=aid)
        else:
            article = Article.objects.all().last()
        categories = Category.objects.all().values('name')
        tags = Tag.objects.all().values('name')
        exist_categories = article.get_categories().strip(',')
        exist_tag = article.get_tag().strip(',')
        return render(request, 'admin/article-edit.html', {
            'categories': categories,
            'tags': tags,
            'article': article,
            'exist_categories': exist_categories,
            'exist_tag': exist_tag
        })


class ArticleBodyView(LoginRequiredMixin, View):
    def get(self, request):
        aid = request.GET.get('aid')
        article_body = Article.objects.get(pk=aid).body
        return HttpResponse(article_body)


class ArticleListView(LoginRequiredMixin, ListView):
    queryset = Article.objects.all().order_by('-id')
    template_name = 'admin/article-list.html'
    context_object_name = 'articles'


class TagView(LoginRequiredMixin, View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, 'admin/tag.html', {'tags': tags})

    def post(self, request):
        tags = request.POST.get('tags', '')
        for tag in tags.split(','):
            try:
                Tag.objects.get_or_create(name=tag.capitalize())
            except Exception:
                pass
        return HttpResponseRedirect(reverse('admin:tag'))

    @myLog
    def delete(self, request):
        logger.info('Try to delete tag')
        tag = json.loads(request.body)
        logger.info(tag)
        t = Tag.objects.get(name=tag['name'])
        tid = t.id
        t.delete()
        return HttpResponse(json.dumps({'tid': tid}))

    def put(self, request):
        data = json.loads(str(request.body, encoding='utf-8'))
        tag = Tag.objects.get(pk=data['id'])
        tag.name = data['val']
        tag.save()
        return HttpResponse(json.dumps(data))


class CategoryView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'admin/categories.html', {'categories': categories})

    def post(self, request):
        categories = request.POST.get('categories', '')
        for categorie in categories.split(','):

            try:
                Category.objects.create(name=categorie.capitalize())
            except Exception:
                pass
        return HttpResponseRedirect(reverse('admin:categories'))

    @myLog
    def delete(self, request):
        categories = json.loads(request.body)
        c = Category.objects.get(name=categories['name'])
        cid = c.id
        c.delete()
        return HttpResponse(json.dumps({'cid': cid}))

    def put(self, request):
        data = json.loads(str(request.body, encoding='utf-8'))
        categories = Category.objects.get(pk=data['id'])
        categories.name = data['val']
        categories.save()
        return HttpResponse(json.dumps(data))


class UploadView(FormView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.get('editormd-image-file', None)
        if files:
            img = Images.objects.create(image=files)
            result = {'success': 1, 'message': 'OK',
                      'url': request.META['HTTP_ORIGIN'] + settings.MEDIA_URL + str(img.image)}
        else:
            result = {'success': 0, 'message': '未获取到文件！'}
        return HttpResponse(json.dumps(result), content_type='application/json')


class LinkView(LoginRequiredMixin, View):
    def get(self, request):
        links = Link.objects.all().order_by('-add_time')
        return render(request, 'admin/link.html', {'links': links})

    def post(self, request):
        link_form = LinkForm(request.POST)
        if link_form.is_valid():
            link_form.save()
            return HttpResponseRedirect(reverse('admin:link'))
        else:
            return HttpResponse(link_form.errors)

    def delete(self, request):
        link = json.loads(str(request.body, encoding='utf-8'))
        l = Link.objects.get(pk=link['lid'])
        lid = l.id
        l.delete()
        return HttpResponse(json.dumps({'lid': lid}))

    def put(self, request):
        data = json.loads(str(request.body, encoding='utf-8'))
        link = Link.objects.get(pk=data['lid'])
        link.description = data['description']
        link.url = data['url']
        link.name = data['name']
        link.save()
        return HttpResponse(json.dumps(data))


class UsersView(LoginRequiredMixin, ListView):
    queryset = UserProfile.objects.all()
    template_name = 'admin/users.html'
    context_object_name = 'users'


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/profile.html')

    def post(self, request):
        image = request.FILES.get('image')
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        user = UserProfile.objects.get(pk=request.user.pk)
        flag = False
        if image:
            user.image = image
        if nickname and nickname != user.nickname:
            user.nickname = nickname
        if gender and gender != user.gender:
            user.gender = gender
        if email and email != user.email:
            user.email = email
            flag = True
        user.save()
        Message.objects.create(body="用户%s于%s通过后台修改了个人信息" %
                               (user.email, timezone.now()))
        if flag:
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('admin:profile'))


class MessageOSView(LoginRequiredMixin, ListView):
    template_name = 'admin/message-os.html'
    context_object_name = 'messages'

    def get_queryset(self):
        Message.objects.filter(status=False).update(status=True)
        messages = Message.objects.all()
        return messages


class MessageCommentView(LoginRequiredMixin, View):
    def get(self, request):
        BlogComment.objects.filter(status=False).update(status=True)
        comments = BlogComment.objects.all().order_by('-add_time')
        return render(request, 'admin/message-comment.html', {'comments': comments})


class SettingView(View):
    def get(self, request):
        try:
            setting = Setting.objects.get(pk=1)
        except Setting.DoesNotExist:
            setting = None
        return render(request, 'admin/setting.html', {'setting': setting})

    def post(self, request):
        setting_form = SettingForm(request.POST)
        if setting_form.is_valid():
            title = request.POST.get('title')
            keywords = request.POST.get('keywords')
            description = request.POST.get('description')
            nickname = request.POST.get('nickname')
            avatar = request.FILES.get('avatar')
            homedescription = request.POST.get('homedescription')
            recordinfo = request.POST.get('recordinfo')
            statisticalcode = request.POST.get('statisticalcode')
            setting, flag = Setting.objects.get_or_create(pk=1)
            setting.title = title
            setting.keywords = keywords
            setting.description = description
            setting.nickname = nickname
            if avatar:
                setting.avatar = avatar
            setting.homedescription = homedescription
            setting.recordinfo = recordinfo
            setting.statisticalcode = statisticalcode
            setting.save()
            return HttpResponseRedirect(reverse('admin:setting'))
        else:
            return HttpResponse(setting_form.errors)
