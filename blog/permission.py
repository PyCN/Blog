from django.shortcuts import render
from django.db.models import Q
from django.core.urlresolvers import resolve

from blog.models import Permission

def perm_check(request, *args, **kwargs):
    url_obj = resolve(request.path_info)
    url_name = url_obj.url_name
    # 在模板中定义了权限与urlname配合
    if url_name:
        # Get method and args
        url_method, url_args = request.method, request.GET
        url_args_list = []
        for i in url_args:
            url_args_list.append(str(url_args[i]))
        url_args_list = ','.join(url_args_list)

        perm_data = Permission.objects.filter(Q(url=url_name) and Q(per_method=url_method) and Q(argument_list=url_args_list))
        if perm_data:
            for perm in perm_data:
                if request.user.has_perm('blog.%s' % perm.name):
                    return True
    return False


def check_blog_permission(fun):
    def wapper(request, *args, **kwargs):
        if perm_check(request, *args, **kargs):
            return fun(request, *args, **kargs)
        return render(request, '403.html')
    return wapper
