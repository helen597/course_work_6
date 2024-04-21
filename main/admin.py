from django.contrib import admin
from main.models import Client, Message, Sending, Trial

# Register your models here.
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Sending)
admin.site.register(Trial)
