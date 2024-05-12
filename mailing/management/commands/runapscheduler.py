import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util


logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Hello')
