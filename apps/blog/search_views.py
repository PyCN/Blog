#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from haystack.views import SearchView
from django.shortcuts import Http404

from blog.models import Article, Category, Tag, BlogComment, UserProfile,\
    VisitorIP
from blog.views import get_context_data_all


logger = logging.getLogger('web')


class MySearchView(SearchView):

    def __call__(self, request):
        self.template = 'blog/index.html'
        try:
            super(MySearchView, self).__call__(request)
            result = self.create_response()
        except Exception, e:
            logger.error('search error: %s', e)
            raise Http404
        return result

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context = get_context_data_all()
        return context
