from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a default superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='lokesh').exists():
            User.objects.create_superuser(
                username='lokesh',
                email='',
                password='lokesh@123'
            )
            self.stdout.write(self.style.SUCCESS('Default superuser created: lokesh / lokesh@123'))
        else:
            self.stdout.write('Superuser lokesh already exists')
