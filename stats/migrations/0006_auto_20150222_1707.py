# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20150222_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenhouplayer',
            name='rank',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
