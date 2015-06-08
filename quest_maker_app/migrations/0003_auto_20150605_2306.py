# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quest_maker_app', '0002_auto_20150605_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
