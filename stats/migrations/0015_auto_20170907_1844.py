# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0014_remove_tenhouplayer_waml_group'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tenhouplayer',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='tenhouplayer',
            name='primary_id',
        ),
        migrations.RemoveField(
            model_name='tenhougame',
            name='players',
        ),
        migrations.DeleteModel(
            name='TenhouPlayer',
        ),
    ]
