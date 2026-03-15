"""
Django management command to create CMS Admins group and assign current user.
Usage: python manage.py seed_cms_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Create CMS Admins group and assign current user'

    def handle(self, *args, **options):
        # Create CMS Admins group
        group, created = Group.objects.get_or_create(name='CMS Admins')

        # Get first superuser or prompt to create one
        user = User.objects.filter(is_superuser=True).first()

        if not user:
            self.stdout.write('No superuser found. Please create a superuser first:')
            self.stdout.write('python manage.py createsuperuser')
            return

        # Add user to CMS Admins group
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(f'OK - CMS Admins group created/verified'))
        self.stdout.write(self.style.SUCCESS(f'OK - User "{user.username}" added to CMS Admins group'))
        self.stdout.write(self.style.SUCCESS(f'You can now access the CMS at: /cms/'))
