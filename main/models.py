from datetime import datetime, timedelta
from django.db import models
from config import settings


NULLABLE = {'null': 'True', 'blank': 'True'}


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    comment = models.CharField(max_length=100, verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('email',)


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='тема письма')
    text = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              **NULLABLE)

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ('theme',)


class Sending(models.Model):
    sent_at = models.DateTimeField(verbose_name='дата и время первой отправки', **NULLABLE)
    period_choices = {"раз в день": "раз в день", "раз в неделю": "раз в неделю", "раз в месяц": "раз в месяц"}
    period = models.CharField(max_length=12, choices=period_choices, default="раз в день", verbose_name='периодичность')
    status_choices = {"created": "создана", "executing": "запущена", "finished": "завершена"}
    status = models.CharField(max_length=15, choices=status_choices, default="создана", verbose_name='статус')
    message = models.ForeignKey("Message", on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              **NULLABLE)
    start_at = models.DateTimeField(default=datetime.now, verbose_name='дата начала')
    finish_at = models.DateTimeField(default=datetime.now()+timedelta(days=30), verbose_name='дата окончания')
    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('sent_at',)


class Trial(models.Model):
    sending = models.ForeignKey("Sending", on_delete=models.CASCADE, verbose_name='рассылка')
    last_tried_at = models.DateTimeField(auto_now_add=True, verbose_name='последняя попытка')
    status = models.BooleanField(default=False, verbose_name='статус')
    server_response = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE )

    def __str__(self):
        str = f'{self.sending} {self.last_tried_at} '
        if self.status:
            str += 'успешная попытка отправки'
        else:
            str += f'ошибка: {self.server_response}'
        return str

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ('last_tried_at',)
