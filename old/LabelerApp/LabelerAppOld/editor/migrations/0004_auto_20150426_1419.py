# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_myparse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myparse',
            name='linkString',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
