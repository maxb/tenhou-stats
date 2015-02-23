# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20150222_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhouplayer',
            name='epoch',
            field=models.CharField(default='lmc-season-2', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tenhouplayer',
            name='tenhou_name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='tenhouplayer',
            unique_together=set([('epoch', 'tenhou_name')]),
        ),
    ]
