# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20150222_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenhougame',
            name='date_played',
        ),
        migrations.AddField(
            model_name='tenhougame',
            name='when_played',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
            preserve_default=False,
        ),
    ]
