# Generated by Django 5.0.4 on 2024-04-21 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_sending_clients_alter_sending_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sending',
            name='clients',
            field=models.ManyToManyField(blank='True', null='True', to='main.client', verbose_name='клиенты'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='message',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.CASCADE, to='main.message', verbose_name='сообщение'),
        ),
    ]
