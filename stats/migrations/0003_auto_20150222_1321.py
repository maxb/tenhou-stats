# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_tenhougame_lobby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenhougame',
            name='game_id',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tenhouplayer',
            name='tenhou_name',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
