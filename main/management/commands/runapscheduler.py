import logging
from datetime import timedelta, datetime
import pytz
from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from main.models import Sending, Trial

logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job(), 'interval', seconds=10)
    scheduler.start()


def my_job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    sendings = Sending.objects.all().filter(status='created').filter(is_active=True)
    sendings.filter(start_at__lte=current_datetime).filter(finish_at__gte=current_datetime)

    for sending in sendings:
        sending.status = 'executing'
        sending.save()
        email_list = [client.email for client in sending.clients.all()]

        result = send_mail(
            subject=sending.message.theme,
            message=sending.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=False,
        )

        trial = Trial(sending=sending, status=result)
        trial.save()

        if not sending.sent_at and result:
            sending.sent_at = current_datetime

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


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        print("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            print("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            print("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
            print("Scheduler shut down successfully!")
