# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_auto_20150306_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenhouplayer',
            name='waml_group',
            field=models.CharField(blank=True, max_length=1),
            preserve_default=True,
        ),
    ]
