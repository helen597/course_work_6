from django.contrib import admin
from main.models import Client, Message, Sending, Trial

# Register your models here.
admin.site.register(Client, Message, Sending, Trial)
