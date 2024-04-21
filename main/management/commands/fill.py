from django.core.management import BaseCommand
import json
from main.models import Client, Message, Sending


class Command(BaseCommand):
    def handle(self, *args, **options):

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
                sendings_to_create.append(Sending(message=message, clients=item['fields']['clients']))

        Sending.objects.bulk_create(sendings_to_create)
