# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0001_initial'),
        ('dojobites_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dojobites_app.Date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_reg_app.User')),
            ],
        ),
    ]