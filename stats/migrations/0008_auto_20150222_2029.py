# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_auto_20150222_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhouplayer',
            name='nbaiman',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='ndays',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='ngames',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nhaneman',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nmangan',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nplace1',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nplace2',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nplace3',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nplace4',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nsanbaiman',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenhouplayer',
            name='nyakuman',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
