"""
WSGI config for blog_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import logging
import logging.config
from os.path import join, dirname, abspath

from django.core.wsgi import get_wsgi_application

from configs.log_config import log_setting

PROJECT_DIR = dirname(abspath(__file__))
sys.path.append(PROJECT_DIR)

os.environ["DJANGO_SETTINGS_MODULE"] = "configs.settings"

logging.config.dictConfig(log_setting)
logger = logging.getLogger('web')

logger.info('Web start!')
application = get_wsgi_application()

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
