# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gscrapweb', '0002_tracks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.TextField()),
                ('author_link', models.TextField()),
                ('track_type', models.TextField()),
                ('title', models.TextField()),
                ('link', models.TextField()),
                ('thumbnail', models.TextField()),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='tracks',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Tracks',
        ),
    ]
