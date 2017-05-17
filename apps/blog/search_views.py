#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack.views import SearchView

from blog.models import Article, Category, Tag, BlogComment, UserProfile,\
    VisitorIP
from blog.views import get_context_data_all


class MySearchView(SearchView):

    def __call__(self, request):
        self.template = 'blog/index.html'
        super(MySearchView, self).__call__(request)
        return self.create_response()

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context = get_context_data_all()
        return context
