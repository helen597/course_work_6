# Generated by Django 5.0.4 on 2024-04-21 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_sending_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='sending',
            name='finish_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='дата окончания'),
        ),
        migrations.AddField(
            model_name='sending',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
        migrations.AddField(
            model_name='sending',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='дата начала'),
        ),
    ]