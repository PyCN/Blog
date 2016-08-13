# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160812_1357'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
