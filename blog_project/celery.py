from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')  
app = Celery('blog_project')  

# Using a string here means the worker will not have to  
# pickle the object when using Windows.  
app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
)

@app.task(bind=True)  
def debug_task(self):  
    print('Request: {0!r}'.format(self.request))  
