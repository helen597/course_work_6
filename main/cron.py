import smtplib
from django.core.mail import send_mail
from django.conf import settings
from main.models import Sending, Trial
from datetime import datetime, timedelta
import pytz


def my_scheduled_job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    sendings = Sending.objects.all().filter(status='created').filter(is_active=True).filter(start_at__lte=current_datetime).filter(finish_at__gte=current_datetime)

    for sending in sendings:
        sending.status = 'executing'
        sending.save()
        email_list = [client.email for client in sending.clients.all()]

        try:
            server_response = send_mail(
                subject=sending.message.theme,
                message=sending.message.text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=email_list,
                fail_silently=False,
            )

            trial = Trial(sending=sending, status=True, server_response=server_response)
            trial.save()

            if not sending.sent_at:
                sending.sent_at = current_datetime

        except smtplib.SMTPException as e:
            trial = Trial(sending=sending, status=False, server_response=e)
            trial.save()

        finally:
            if sending.period == 'раз в день':
                sending.start_at = trial.last_tried_at + timedelta(days=1)
            elif sending.period == 'раз в неделю':
                sending.start_at = trial.last_tried_at + timedelta(weeks=1)
            elif sending.period == 'раз в месяц':
                sending.start_at = trial.last_tried_at + timedelta(days=30)

            if sending.start_at < sending.finish_at:
                sending.status = 'created'
            else:
                sending.status = 'finished'
                sending.is_active = False
            sending.save()
