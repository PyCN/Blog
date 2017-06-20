#!/usr/bin/env python
import os
import sys
import logging
import logging.config


from configs.log_config import log_setting

logging.config.dictConfig(log_setting)
logger = logging.getLogger('web')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

    logger.info('Web start!')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
