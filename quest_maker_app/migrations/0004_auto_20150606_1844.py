# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quest_maker_app', '0003_auto_20150605_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyDistance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('miles', models.FloatField(null=True, blank=True)),
                ('day', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='dailymile',
            name='user',
        ),
        migrations.AddField(
            model_name='quest',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 43, 58, 893156, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quest',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 6, 323494, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questtemplate',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 15, 935755, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questtemplate',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 22, 489524, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userquest',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 31, 962146, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userquest',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 37, 119534, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waypoint',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 43, 114392, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waypoint',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 23, 44, 46, 678660, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DailyMile',
        ),
    ]
