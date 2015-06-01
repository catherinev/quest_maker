# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quest_maker_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waypoint',
            name='notability',
            field=models.CharField(default='medium', max_length=10, choices=[(b'high', b'high'), (b'medium', b'medium'), (b'low', b'low')]),
            preserve_default=False,
        ),
    ]
