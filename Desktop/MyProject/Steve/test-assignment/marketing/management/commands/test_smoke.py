"""
Django management command to run smoke tests.
Usage: py manage.py test_smoke
"""

from django.core.management.base import BaseCommand
from django.test.utils import get_runner
from django.conf import settings


class Command(BaseCommand):
    help = 'Run smoke tests for critical functionality'

    def handle(self, *args, **options):
        """Run smoke tests and display results."""
        self.stdout.write(self.style.SUCCESS('Running smoke tests...'))
        self.stdout.write('')

        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)

        # Run smoke tests
        test_labels = ['marketing.tests.test_smoke_working']
        failures = test_runner.run_tests(test_labels)

        if failures:
            self.stdout.write(self.style.ERROR('Smoke tests FAILED!'))
            self.stdout.write(self.style.WARNING('Fix critical issues before committing.'))
        else:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('PASS: All smoke tests passed!'))
            self.stdout.write(self.style.SUCCESS('Critical functionality verified.'))
