from datetime import datetime, timedelta
from .models import NewsLetter, SendAttemp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
import pytz
import logging

from .services import send_email

logger = logging.getLogger(__name__)

def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = NewsLetter.objects.filter(create_date__lte=current_datetime, is_published=True, status=NewsLetter.LAUNCHED)

    for mailing in mailings:
        last_attempt = SendAttemp.objects.filter(newsletter=mailing).order_by('-attempt_date').first()
        next_send_time = current_datetime

        if mailing.frequency == NewsLetter.DAILY:
            next_send_time = last_attempt.attempt_date + timedelta(days=1) if last_attempt else current_datetime
        elif mailing.frequency == NewsLetter.WEEKLY:
            next_send_time = last_attempt.attempt_date + timedelta(weeks=1) if last_attempt else current_datetime
        elif mailing.frequency == NewsLetter.MONTHLY:
            next_send_time = last_attempt.attempt_date + timedelta(weeks=4) if last_attempt else current_datetime

        if current_datetime >= next_send_time:
            send_email(mailing.message.subject, mailing.message.body, [client.email for client in mailing.client.all()])
            SendAttemp.objects.create(newsletter=mailing, attempt_date=current_datetime)


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
    send_mailing,
    trigger=CronTrigger(minute='*/10'),
    id='send_mailing',
    max_instances=1,
    replace_existing=True,
)
    logger.info("Added job 'send_mailing'.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped.")

