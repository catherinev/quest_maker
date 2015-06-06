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
            name='DailyMile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('miles', models.FloatField(null=True, blank=True)),
                ('day', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('start_date', models.DateField(auto_now=True)),
                ('leader', models.ForeignKey(related_name='quests_led', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='quest_templates_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserQuest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.CharField(max_length=100)),
                ('total_miles', models.FloatField()),
                ('quest', models.ForeignKey(related_name='user_quests', to='quest_maker_app.Quest')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('distance_from_start', models.FloatField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('notability', models.CharField(max_length=10, choices=[(b'high', b'high'), (b'medium', b'medium'), (b'low', b'low')])),
                ('quest_template', models.ForeignKey(to='quest_maker_app.QuestTemplate')),
            ],
        ),
        migrations.AddField(
            model_name='quest',
            name='template',
            field=models.ForeignKey(to='quest_maker_app.QuestTemplate'),
        ),
        migrations.AddField(
            model_name='quest',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='quest_maker_app.UserQuest'),
        ),
    ]
