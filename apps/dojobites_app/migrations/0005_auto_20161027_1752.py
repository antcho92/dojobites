# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojobites_app', '0004_auto_20161027_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
