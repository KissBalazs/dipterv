# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0002_mypost_labels'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyParse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linkString', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
