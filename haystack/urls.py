from django.conf.urls import url  
from haystack.views import SearchView  
import search_views

urlpatterns = [  
    url(r'^$', search_views.MySearchView(), name='haystack_search'),  
]  