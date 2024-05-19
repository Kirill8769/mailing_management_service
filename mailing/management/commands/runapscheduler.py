import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from mailing.models import Mailing, Log


logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)


def change_status():
    mailings = Mailing.objects.all()
    if mailings:
        for mailing in mailings:
            if mailing.end_date < timezone.now():
                mailing.mailing_status = 'E'
                if scheduler.get_job(str(mailing.pk)):
                    scheduler.remove_job(str(mailing.pk))
                    logger.info(f"Рассылка {mailing.title} завершена")
            elif mailing.mailing_status == 'S':
                if scheduler.get_job(str(mailing.pk)):
                    scheduler.remove_job(str(mailing.pk))
                    logger.info(f"Рассылка {mailing.title} остановлена")
            elif mailing.start_date <= timezone.now() <= mailing.end_date:
                if not mailing.owner.is_active:
                    mailing.mailing_status = 'S'
                else:
                    mailing.mailing_status = 'R'
            mailing.save()


def start_or_not_mailing():
    mailings_correct = Mailing.objects.filter(mailing_status='R')
    if mailings_correct:
        for mailing in mailings_correct:
            # Добавить проверку на необходимость добавления задания по дате отправки и периоду
            add_job(mailing)


def send_mailings(mailing):
    title = mailing.message.subject
    message = mailing.message.body
    from_email = settings.DEFAULT_FROM_EMAIL
    clients = mailing.client.all()
    if clients:
        for client in clients:
            try:
                send_status = send_mail(title, message, from_email, (client.email, ))
                if send_status:
                    Log.objects.create(
                        attempt_status='Y',
                        answer_server='Успешно',
                        client=client,
                        mailing=mailing,
                        owner=mailing.owner,
                    )
                else:
                    Log.objects.create(
                        attempt_status='N',
                        answer_server='Ошибка',
                        client=client,
                        mailing=mailing,
                        owner=mailing.owner,
                    )
            except Exception as ex:
                Log.objects.create(
                    attempt_status='N',
                    answer_server=f'{ex}',
                    client=client,
                    mailing=mailing,
                    owner=mailing.owner,
                )


def add_job(mailing):
    if mailing.periodicity == 'D':
        # cron_period = CronTrigger(day='*/1')
        cron_period = CronTrigger(second='*/30')
    elif mailing.periodicity == 'W':
        # cron_period = CronTrigger(week='*/1')
        cron_period = CronTrigger(second='*/30')
    else:
        # cron_period = CronTrigger(month='*/1')
        cron_period = CronTrigger(second='*/30')
    scheduler.add_job(
        send_mailings,
        trigger=cron_period,
        id=f'{mailing.pk}',
        max_instances=1,
        args=[mailing],
        replace_existing=True,
    )


class Command(BaseCommand):
    help = "Runs APSscheduler"

    def handle(self, *args, **options):

        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            change_status,
            trigger=CronTrigger(second='*/30'),
            id='change_status',
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'change_status'.")

        scheduler.add_job(
            start_or_not_mailing,
            trigger=CronTrigger(second='*/30'),
            id='start_or_not_mailing',
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'start_or_not_mailing'.")

        try:
            logger.info('Starting scheduler')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler')
            scheduler.shutdown()
            logger.info('Scheduler shutdown successfully!')
