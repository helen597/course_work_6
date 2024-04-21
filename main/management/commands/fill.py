import os
from django.core.management import BaseCommand
import json
from django.db import connection

from main.models import Client, Message, Sending


class Command(BaseCommand):
    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE main_message RESTART IDENTITY CASCADE;')

        Client.objects.all().delete()
        Message.objects.all().delete()
        Sending.objects.all().delete()

        with open('data.json', 'r') as f:
            data = json.load(f)

        clients_to_create = []
        messages_to_create = []
        sendings_to_create = []

        for item in data:
            if item["model"] == "main.client":
                clients_to_create.append(Client(**item['fields']))
            elif item["model"] == "main.message":
                messages_to_create.append(Message(**item['fields']))

        Client.objects.bulk_create(clients_to_create)
        print(clients_to_create)
        Message.objects.bulk_create(messages_to_create)
        print(messages_to_create)

        for item in data:
            if item["model"] == "main.sending":
                message = Message.objects.get(pk=item['fields']['message'])
                s = Sending(message=message)
                s.save()
                s.clients.set(item['fields']['clients'])
                sendings_to_create.append(s)

        Sending.objects.bulk_create(sendings_to_create)
