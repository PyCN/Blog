#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack.views import SearchView

from blog.models import Article, Category, Tag, BlogComment, UserProfile


class MySearchView(SearchView):

    def __call__(self, request):
        self.template = 'blog/index.html'
        super(MySearchView, self).__call__(request)
        return self.create_response()

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['category_list'] = Category.objects.all()
        context['date_archive'] = Article.objects.archive()
        context['tag_list'] = Tag.objects.all()
        return context