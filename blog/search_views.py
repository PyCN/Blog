#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack.views import SearchView


class MySearchView(SearchView):

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        return context