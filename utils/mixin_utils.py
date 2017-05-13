#coding:utf-8

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LoginRequiredMixin(object):
    """用户登录验证"""

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        deny_url = ('admin/article/add/',
                    '/admin/article/list/',
                    'article/edit/',
                    'article/body/',
                    '/admin/tag/',
                    '/admin/categories/',
                    '/admin/message/comment/',
                    '/admin/message/os/',
                    '/admin/users/',
                    '/admin/link/',
                    '/admin/setting/')
        if request.path in deny_url:
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
