# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TenhouGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('game_id', models.CharField(max_length=255)),
                ('date_played', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TenhouPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('tenhou_name', models.CharField(max_length=255)),
                ('primary_id', models.ForeignKey(to='stats.TenhouPlayer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tenhougame',
            name='players',
            field=models.ManyToManyField(to='stats.TenhouPlayer'),
            preserve_default=True,
        ),
    ]
