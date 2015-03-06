# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_epoch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenhougame',
            name='players',
            field=models.ManyToManyField(to='stats.TenhouPlayer', blank=True),
            preserve_default=True,
        ),
    ]
