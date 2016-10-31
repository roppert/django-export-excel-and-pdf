# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('max', models.DecimalField(decimal_places=2, max_digits=4)),
                ('mean', models.DecimalField(decimal_places=2, max_digits=4)),
                ('min', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='temperature',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.WeatherStation'),
        ),
    ]