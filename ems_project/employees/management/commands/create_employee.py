from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from employees.models import Employee
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an Employee record for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('--department', type=str, default='IT', help='Department (default: IT)')
        parser.add_argument('--designation', type=str, default='Employee', help='Designation (default: Employee)')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found'))
            return
        
        if Employee.objects.filter(user=user).exists():
            self.stdout.write(self.style.WARNING(f'Employee record already exists for "{username}"'))
            return
        
        employee = Employee.objects.create(
            user=user,
            department=options['department'],
            designation=options['designation'],
            joining_date=date.today()
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Employee record created for "{username}"'))
