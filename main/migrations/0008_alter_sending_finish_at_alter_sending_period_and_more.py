# Generated by Django 5.0.4 on 2024-04-22 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_client_owner_message_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sending',
            name='finish_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 22, 21, 12, 36, 439701), verbose_name='дата окончания'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='period',
            field=models.CharField(choices=[('раз в день', 'раз в день'), ('раз в неделю', 'раз в неделю'), ('раз в месяц', 'раз в месяц')], default='раз в день', max_length=12, verbose_name='периодичность'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='status',
            field=models.CharField(choices=[('created', 'создана'), ('executing', 'запущена'), ('finished', 'завершена')], default='создана', max_length=15, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='server_response',
            field=models.CharField(blank='True', null='True', verbose_name='ответ почтового сервера'),
        ),
    ]