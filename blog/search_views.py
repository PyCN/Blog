#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack.views import SearchView


class MySearchView(SearchView):

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context.update({'first':'first'})
        return context
    
    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        with open('/home/ctg/django.txt', 'w') as f:
            f.write(str(queryset))
            f.write(dir(queryset))
        return ''