# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='labels',
            field=models.CharField(default='nincs', max_length=200),
            preserve_default=False,
        ),
    ]
