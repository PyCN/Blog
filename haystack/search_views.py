#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blog.models import Article
from haystack.views import SearchView


class MySearchView(SearchView):

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        return context
    
    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        return queryset