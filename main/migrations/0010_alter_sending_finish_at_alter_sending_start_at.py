# Generated by Django 5.0.4 on 2024-04-22 20:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_sending_options_alter_sending_finish_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sending',
            name='finish_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 22, 20, 8, 33, 826261, tzinfo=datetime.timezone.utc), verbose_name='дата окончания'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 22, 20, 8, 33, 826261, tzinfo=datetime.timezone.utc), verbose_name='дата начала'),
        ),
    ]