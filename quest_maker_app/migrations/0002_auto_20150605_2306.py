# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quest_maker_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 6, 6, 4, 6, 3, 717390, tzinfo=utc)),
        ),
    ]
