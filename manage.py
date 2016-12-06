#!/usr/bin/env python
import os
import sys
import logging

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                        filename='blog.log')
    logging.info('Web start!')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
