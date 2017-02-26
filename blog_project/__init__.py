from __future__ import absolute_import

import logging

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                    filename='blog.log')
logging.info('Web start!')
from .celery import app as celery_app
