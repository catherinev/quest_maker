# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('creator', models.ForeignKey(related_name='quests_created', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='quests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('distance_from_start', models.FloatField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('quest', models.ForeignKey(to='quest_maker_app.Quest')),
            ],
        ),
    ]
