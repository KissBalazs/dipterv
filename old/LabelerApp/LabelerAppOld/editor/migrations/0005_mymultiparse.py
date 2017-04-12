# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0004_auto_20150426_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyMultiParse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linkTexts', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
