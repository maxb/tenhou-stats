# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20150222_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhougame',
            name='scores',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhougame',
            name='url_names',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
