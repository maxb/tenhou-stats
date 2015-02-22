# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20150222_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhouplayer',
            name='rank',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='rank_time',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='rate',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
