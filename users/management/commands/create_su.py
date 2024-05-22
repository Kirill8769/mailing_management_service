from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """ Команда для создания суперпользователя """

    def handle(self, *args, **options):
        """ Метод обработки команды """

        user = User.objects.create(email='admin')
        user.set_password('12345')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
