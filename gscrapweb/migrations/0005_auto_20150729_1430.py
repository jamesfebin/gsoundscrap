# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gscrapweb', '0004_track_embed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
