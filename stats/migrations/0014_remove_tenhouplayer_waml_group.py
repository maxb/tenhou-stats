# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0013_tenhouplayer_waml_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenhouplayer',
            name='waml_group',
        ),
    ]
