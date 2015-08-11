# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quest_maker_app', '0006_auto_20150723_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailydistance',
            name='manually_entered',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 2, 46, 24, 482207), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 2, 46, 31, 507357), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quest',
            name='hours_offset_utc',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quest',
            name='users_last_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 2, 46, 48, 387404)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dailydistance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='dailydistance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='quest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='quest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='questtemplate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='questtemplate',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userquest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userquest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='waypoint',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='waypoint',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='dailydistance',
            unique_together=set([('user', 'day')]),
        ),
        migrations.AlterUniqueTogether(
            name='userquest',
            unique_together=set([('user', 'quest')]),
        ),
    ]
