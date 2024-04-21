# Generated by Django 5.0.4 on 2024-04-21 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_sending_finish_at_sending_is_active_sending_start_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sending',
            name='clients',
            field=models.ManyToManyField(default={}, to='main.client', verbose_name='клиенты'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='message',
            field=models.ForeignKey(default={}, on_delete=django.db.models.deletion.CASCADE, to='main.message', verbose_name='сообщение'),
        ),
    ]
