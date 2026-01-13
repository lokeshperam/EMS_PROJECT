from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from employees.models import Employee
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a new admin user with Employee record'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('email', type=str, help='Email address')
        parser.add_argument('password', type=str, help='Password')
        parser.add_argument('--first-name', type=str, default='', help='First name')
        parser.add_argument('--last-name', type=str, default='', help='Last name')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options.get('first_name', '')
        last_name = options.get('last_name', '')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists'))
            return
        
        # Create user with admin role
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.role = 'ADMIN'
        user.save()
        
        # Create employee record
        Employee.objects.create(
            user=user,
            department='IT',
            designation='Administrator',
            joining_date=date.today()
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Admin user "{username}" created successfully!'))
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Role: ADMIN')
