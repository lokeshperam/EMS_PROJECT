from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Display all users in the database'

    def handle(self, *args, **options):
        users = User.objects.all()
        self.stdout.write(f'Total users: {users.count()}')
        for user in users:
            self.stdout.write(f'Username: {user.username}, Email: {user.email}, Role: {user.role}, Is Staff: {user.is_staff}, Is Superuser: {user.is_superuser}')
