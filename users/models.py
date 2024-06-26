from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    verification_code = models.CharField(max_length=10, verbose_name='код верификации', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активный')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('email',)
        permissions = [
            ("set_active", "Can block user")
        ]
