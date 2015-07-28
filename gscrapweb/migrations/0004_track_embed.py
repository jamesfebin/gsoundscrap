# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gscrapweb', '0003_auto_20150728_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='embed',
            field=models.TextField(default=b''),
        ),
    ]
