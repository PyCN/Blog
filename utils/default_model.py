from django.utils import timezone


def random_nick_name():
    current = str(timezone.now()).split('.')[0].replace('-', '').replace(':', '').replace(' ', '')
    nick_name = '用户%s' % current
    return nick_name
