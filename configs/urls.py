# coding:utf-8

"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from blog import views
from configs import settings

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^admin/', include('admin.urls', namespace='admin', app_name='admin')),
    url(r'^api/', include(router.urls)),
    url(r'', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    # 如果使用settings.MEDIA_ROOT,那么会上传到media/下，因为settings中的MEDIA_ROOT路径为../Blog/configs
    urlpatterns.append(url(r'^media/(?P<path>.*)$',
                           'django.views.static.serve', {'document_root':
                                                         settings.MEDIA_ROOT}))
