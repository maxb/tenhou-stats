# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0009_auto_20150223_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhougame',
            name='epoch',
            field=models.CharField(max_length=255, default='lmc-season-2'),
            preserve_default=False,
        ),
    ]
