# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quest_maker_app', '0004_auto_20150606_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('fitbit_enabled', models.BooleanField(default=False, editable=False)),
                ('encrypted_fitbit_key', models.CharField(max_length=1000, null=True, editable=False, blank=True)),
                ('encrypted_fitbit_secret', models.CharField(max_length=1000, null=True, editable=False, blank=True)),
                ('encrypted_fitbit_userid', models.CharField(max_length=1000, null=True, editable=False, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
