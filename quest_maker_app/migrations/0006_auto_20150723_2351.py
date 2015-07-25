# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quest_maker_app', '0005_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='encrypted_fitbit_key',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='encrypted_fitbit_secret',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='encrypted_fitbit_userid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='fitbit_enabled',
        ),
    ]
